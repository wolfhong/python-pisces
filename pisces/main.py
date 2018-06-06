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
AJAX_TIME = 0.5  # seconds for implicitly_wait
RETRY_WAIT_TIME = 2  # seconds
PY3 = sys.version_info[0] == 3  # True/False

if PY3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve


# see http://chromedriver.storage.googleapis.com/index.html for chromedriver.
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
if sys.platform.startswith('darwin'):
    CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools', 'chromedriver_mac')
    GECKODRIVER = os.path.join(ROOT_PATH, 'tools', 'geckodriver_mac')
elif sys.platform.startswith('linux'):
    CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools', 'chromedriver_linux')
    GECKODRIVER = os.path.join(ROOT_PATH, 'tools', 'geckodriver_linux')
elif sys.platform in ['win32', 'cygwin']:
    CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools', 'chromedriver.exe')
    GECKODRIVER = os.path.join(ROOT_PATH, 'tools', 'geckodriver.exe')


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
    # can work on 2018/6/5
    _map = {
        'google': '//div[@id="ires"]/div/div[@id="isr_mc"]/div/div/div/div/a/img',
        'bing.com': '//div[@class="dg_b"]//div[@class="img_cont hoff"]/img',
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

    def __init__(self, quiet=False, headless=True, workers=0, browser='chrome'):
        '''
        :param quiet: no output
        :param headless: no UI(no graphical display)
        :param workers: the number of threads when downloading images, `0` means the cpu count
        :param browser: the web-browser, chrome needs ChromeDriver, firefox needs GeckoDriver
        '''
        self.browser = browser.lower()
        assert self.browser in ['firefox', 'chrome', 'ie', 'opera', 'safari', 'phantomjs']

        self.quiet = quiet
        self.workers = int(workers)
        self.headless = headless

        options._options = {'quiet': quiet}  # set global options
        self.driver = self.decide_driver()

    def decide_driver(self):
        if self.browser not in ['firefox', 'chrome']:
            raise AssertionError("only firefox or chrome supported.")
        if self.browser == 'chrome':
            # To see http://chromedriver.storage.googleapis.com/index.html for chromedriver.
            # If it cann't run, please check out chromedriver's version and upgrade to the newest.
            opt = webdriver.chrome.options.Options()
            # bugfix: https://stackoverflow.com/questions/50642308/org-openqa-selenium-webdriverexception-unknown-error-devtoolsactiveport-file-d
            opt.add_argument("--disable-extensions")  # disabling extensions
            opt.add_argument("--disable-gpu")  # applicable to windows os only
            opt.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
            opt.add_argument("--no-sandbox")  # Bypass OS security model
            opt.set_headless(headless=self.headless)  # no graphical display

            params = {'options': opt}
            if os.path.exists(CHROMEDRIVER):  # if not, put it in $PATH
                params['executable_path'] = CHROMEDRIVER
            return webdriver.Chrome(**params)
        elif self.browser == 'firefox':
            opt = webdriver.firefox.options.Options()
            opt.add_argument("--disable-extensions")  # disabling extensions
            opt.add_argument("--disable-gpu")  # applicable to windows os only
            opt.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
            opt.add_argument("--no-sandbox")  # Bypass OS security model
            opt.set_headless(headless=self.headless)

            params = {'options': opt}
            if os.path.exists(GECKODRIVER):  # if not, put it in $PATH
                params['executable_path'] = GECKODRIVER
            return webdriver.Firefox(**params)

    def close(self):
        if self.driver and hasattr(self.driver, 'quit'):
            self.driver.quit()
            self.driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

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

    def download_by_url(self, url, output_dir, image_count=100):
        '''
        :param url: url in web-browser
        :param output_dir: destination to save images
        :param image_count: image count downloaded
        :return: image count downloaded actually
        '''
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # equal to `mkdir -p output_dir`

        driver = self.driver
        driver.maximize_window()  # TODO: not work on mac
        driver.get(url)

        xpath = get_xpath_by_url(url)
        add_image_count = 0
        empty_retry_count = 3
        loop_zero_count = 0  # the count of getting nothing in a loop

        while add_image_count < image_count:
            # js = "document.documentElement.scrollTop=%d" % pos
            js = "window.scrollTo(0, document.body.scrollHeight);"
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

            driver.execute_script(js)  # scrollDown in advance
            if loop_image_list:
                self.download_threading(loop_image_list)
            if loop_image_count == 0:
                loop_zero_count += 1
                if loop_zero_count > empty_retry_count:
                    break
                print_msg('no more images loaded, try %s ...' % loop_zero_count)
                time.sleep(RETRY_WAIT_TIME)
        return add_image_count

    def download_by_word(self, word, output_dir, engine='google', image_count=100):
        '''
        search images by `word` using `engine`, download images to `output_dir`
        :param word: keyword to search images
        :param engine: search engine, choice in google/bing/yahoo/baidu/sogou/360
        '''
        url = get_url_by_word_engine(word, engine)
        return self.download_by_url(url, output_dir, image_count=image_count)
