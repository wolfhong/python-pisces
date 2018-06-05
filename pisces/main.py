#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see https://www.seleniumhq.org/download for more info.
from __future__ import unicode_literals, print_function
import os
import sys
import uuid
import time
import traceback
from multiprocessing.dummy import Pool
import requests
from selenium import webdriver

DEBUG = True
DOWNLOAD_TIMEOUT = 5  # seconds
AJAX_TIME = 2  # seconds for implicitly_wait
RETRY_WAIT_TIME = 2  # seconds
PY3 = True if sys.version_info[0] == 3 else False

if PY3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve


# see http://chromedriver.storage.googleapis.com/index.html for chromedriver.
ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if sys.platform == 'darwin':
    CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools/chromedriver_mac')
elif sys.platform == 'linux':
    CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools/chromedriver_linux')
elif sys.platform in ['win32', 'cygwin']:
    CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools/chromedriver.exe')


class GlobalOptions(object):
    def __init__(self, options=None):
        self._options = options

    def __getattr__(self, name):
        if name in dir(GlobalOptions) or name in self.__dict__:
            return getattr(self, name)
        elif name in self._options:
            return self._options[name]
        else:
            raise AttributeError("'%s' has no attribute '%s'" % (
                self.__class__.__name__, name))

options = GlobalOptions()


def get_filepath(output_dir, index):
    ''' all format images are rename to *.jpg, regardless of png, bmp or others '''
    filename = '%s_%s.jpg' % (index, uuid.uuid4().__str__().replace('-', ''))
    return os.path.join(output_dir, filename)


def get_xpath_by_url(url):
    '''
    :param url: image page's url of a certain image-search-engine
    :return: xpath of images
    '''
    substring = url[:url.index('/', len('https://'))]
    _map = {
        'google': '//div[@id="ires"]/div/div[@id="isr_mc"]/div/div/div/div/a/img',
        'bing.com': '//div[@id="dg_c"]/div/div[@class="imgres"]/div/div/a/img',
        'yahoo': '//div[@id="res-cont"]/section/div/ul/li/a/img',
        'baidu': '//div[@id="imgid"]/div/ul/li/div/a/img',  # baidu, china
        'sogou': '//div[@id="imgid"]/ul/li/a/img',  # sogou, china
        'so.com': '//div[@id="waterfallX"]/div/ul/li/a/img',  # 360, china
    }
    for k in _map.keys():
        if k in substring:
            return _map[k]
    raise AssertionError('%s is not defined in %s.' % (substring, _map.keys()))


def get_url_by_word_engine(word, engine):
    '''
    :param word: keyword to search images
    :param engine: search engine, choice in google/bing/yahoo/baidu/sogou/360
    '''
    engine = engine.lower()
    _map = {
        'google': 'https://www.google.com/search?q=%s&tbm=isch' % word,
        'bing': 'http://www.bing.com/images/search?q=%s&FORM=IGRE' % word,
        'yahoo': 'https://sg.images.search.yahoo.com/search/images?p=%s' % word,
        'baidu': 'http://image.baidu.com/search/index?tn=baiduimage&word=%s' % word,
        'sogou': 'http://pic.sogou.com/pics?query=%s' % word,
        '360': 'http://image.so.com/i?q=%s' % word,
    }
    if engine not in _map:
        raise AssertionError('%s is not defined in %s.' % (engine, _map.keys()))
    return _map[engine]


def print_msg(msg):
    if not options.quiet:
        print(msg)


def _download_image(a_tuple):
    img_url, filepath = a_tuple
    try:
        if img_url.startswith('data:'):  # base64 encoding image, startswith `data:`
            urlretrieve(img_url, filepath)
            img_url = 'data:<base64>'
        else:
            # urlretrieve(img_url, filepath)  # 403 on py3.6(NT) with baidu, changed to `requests` lib
            headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36;'}
            r = requests.get(img_url, headers=headers, stream=True, timeout=DOWNLOAD_TIMEOUT)
            with open(filepath, 'wb') as f_write:
                for chunk in r.iter_content(1024 * 1024):
                    f_write.write(chunk)
        # end if-else
        print_msg('save %s to %s' % (img_url, filepath))
    except:
        if DEBUG:
            print_msg(traceback.format_exc())
        print_msg('fail to download %s' % img_url)


class Pisces(object):

    def __init__(self, quiet=False, browser=None, workers=0):
        '''
        :param quiet: no output
        :param browser: web-browser to use, firefox/chrome/ie/opera/safari/phantomjs
        :param workers: the number of threads when downloading images, `0` means the cpu count
        '''
        self.quiet = quiet
        options._options = {'quiet': quiet}  # set global options
        browser = (browser or 'firefox').lower()
        assert browser in ['firefox', 'chrome', 'ie', 'opera', 'safari', 'phantomjs']
        self.browser = browser
        self.workers = int(workers)

    def decide_driver(self):
        if self.browser == 'chrome':
            # To see http://chromedriver.storage.googleapis.com/index.html for chromedriver.
            # If it cann't run, please check out chromedriver's version and upgrade to the newest.
            driver = webdriver.Chrome(CHROMEDRIVER)
        else:
            driver = getattr(webdriver, self.browser.title())()
        return driver

    def download_threading(self, url_path_list):
        # for img_url, filepath in url_path_list:
        #     _download_image((img_url, filepath))
        if self.workers <= 0:
            pool = Pool()  # default to cpu count
        else:
            pool = Pool(self.workers)
        pool.map(_download_image, url_path_list)
        pool.close()
        pool.join()

    def download_by_url(self, url, output_dir, image_count=200):
        '''
        :param url: url in web-browser
        :param output_dir: destination to save images
        :param image_count: image count downloaded
        :return: image count downloaded actually
        '''
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        driver = self.decide_driver()
        driver.maximize_window()  # TODO: no working on mac
        driver.get(url)

        xpath = get_xpath_by_url(url)
        add_image_count = 0
        empty_retry_count = 3
        loop_zero_count = 0  # the count of getting nothing in a loop
        pos = 0  # the position of the scroll bar

        while add_image_count < image_count:
            pos += 500  # scroll down 500px
            js = "document.documentElement.scrollTop=%d" % pos
            driver.execute_script(js)
            driver.implicitly_wait(AJAX_TIME)  # wait n seconds

            loop_image_list = []
            loop_image_count = 0
            for element in driver.find_elements_by_xpath(xpath)[add_image_count:]:
                img_url = element.get_attribute('src')
                if img_url:
                    loop_zero_count = 0  # reset to zero
                    add_image_count += 1  # all add one
                    loop_image_count += 1  # this loop add one
                    filepath = get_filepath(output_dir, add_image_count)
                    loop_image_list.append((img_url, filepath, ))
                    if add_image_count >= image_count:
                        break
            if loop_image_list:
                self.download_threading(loop_image_list)
            if loop_image_count == 0:
                loop_zero_count += 1
                if loop_zero_count > empty_retry_count:
                    break
                print_msg('no more images loaded, try %s ...' % loop_zero_count)
                time.sleep(RETRY_WAIT_TIME)
        # close browser
        if driver and hasattr(driver, 'quit'):
            driver.quit()
        return add_image_count

    def download_by_word(self, word, engine, output_dir, image_count=200):
        '''
        search images by `word` using `engine`, download images to `output_dir`
        :param word: keyword to search images
        :param engine: search engine, choice in google/bing/yahoo/baidu/sogou/360
        '''
        url = get_url_by_word_engine(word, engine)
        return self.download_by_url(url, output_dir, image_count=image_count)
