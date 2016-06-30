#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback
import uuid
import os
import urllib
import requests
from selenium import webdriver

THIS_PATH = os.path.abspath(os.path.dirname(__file__))  # 本文件路径
ROOT_PATH = os.path.abspath(os.path.dirname(THIS_PATH))  # 项目根路径
CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools/chromedriver')


def get_local_path(output_dir, m):
    filename = '%s_%s.jpg' % (m, uuid.uuid4().__str__().replace('-', ''))
    return os.path.join(output_dir, filename)


def get_xpath_by_url(url):
    '''根据url确定搜索引擎,从而确定图片的正则匹配'''
    substring = url[:url.index('/', len('https://'))]
    _map = {
        'sogou': '//div[@id="imgid"]/ul/li/a/img',
        'baidu': '//div[@id="imgid"]/div/ul/li/div/a/img',
        'so.com': '//div[@id="waterfallX"]/div/ul/li/a/img',  # 360搜索
        'yahoo': '//div[@id="res-cont"]/section/div/ul/li/a/img',
        'bing.com': '//div[@id="dg_c"]/div/div[@class="imgres"]/div/div/a/img',
        'google': '//div[@id="ires"]/div/div[@id="isr_mc"]/div/div/div/div/a/img',
    }
    for k in _map.keys():
        if k in substring:
            return _map[k]
    raise AssertionError('can only deal with %s, %s is not defined. you should add by yourself.' % (_map.keys(), substring))


def download_image(img_url, filename):
    if img_url.startswith('data:'):  # google或者百度图片有这种形式的图片,data:image/jpeg;开头
        urllib.urlretrieve(img_url, filename)
        return
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36;'}
    r = requests.get(img_url, headers=headers, stream=True)
    with open(filename, 'wb') as f_write:
        f_write.write(r.raw.read())


def main(url, output_dir, image_count=200, quiet=False, close=True, browser=None):
    '''
    @brief 根据某个搜索地址,下载搜索的图片结果到output_dir,下载上限image_count
    @param url 搜索地址url
    @param output_dir 图片保存路径
    @param image_count 搜索图片的最大值
    @param 是否打印过程输出
    @param 是否在运行结束后关闭浏览器
    @param 使用的浏览器类型,firefox/chrome/ie/opera/safari
    @return 下载的图片数量
    '''
    img_url_dic = {}  # 记录下载过的图片地址，避免重复下载
    pos = 0  # 滚动条位置,模拟滚动窗口以浏览下载更多图片
    m = 1  # 图片编号
    xpath = get_xpath_by_url(url)
    if not os.path.exists(output_dir):  # 确保文件夹存在
        os.system('mkdir -p %s' % output_dir)
    # 启动Firefox浏览器
    browser = (browser or 'firefox').lower()
    assert browser in ['firefox', 'chrome', 'ie', 'opera', 'safari']
    if browser == 'chrome':
        # chromedriver to see http://chromedriver.storage.googleapis.com/index.html
        # If it cannot run, please check the version of chromedriver; I use version=2.9
        os.environ["webdriver.chrome.driver"] = CHROMEDRIVER
        driver = webdriver.Chrome(CHROMEDRIVER)
    else:
        driver = getattr(webdriver, browser.title())()
    # driver = webdriver.Firefox()
    # 最大化窗口，因为每一次爬取只能看到视窗内的图片
    driver.maximize_window()
    # 浏览器打开爬取页面
    driver.get(url)
    while m <= image_count:
        pos += 500  # 每次下滚500px
        js = "document.documentElement.scrollTop=%d" % pos
        driver.execute_script(js)
        driver.implicitly_wait(1)  # wait 1 second

        new_image_add = 0
        for element in driver.find_elements_by_xpath(xpath):
            img_url = element.get_attribute('src')
            # 保存图片到指定路径
            if img_url and img_url not in img_url_dic:
                img_url_dic[img_url] = ''
                new_image_add += 1
                filename = get_local_path(output_dir, m)
                try:
                    download_image(img_url, filename)  # 保存图片
                except:
                    logging.error(traceback.format_exc())
                else:
                    if not quiet:
                        print('save %s to %s' % (img_url, filename))
                    m += 1
                    if m > image_count:
                        break
        if new_image_add == 0:
            raise AssertionError('no more images loaded...')
    # 关闭浏览器该标签页
    if close:
        driver.close()
    return m - 1
