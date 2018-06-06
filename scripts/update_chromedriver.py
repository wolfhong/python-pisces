#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tools/chromedriver is downloaded from http://chromedriver.storage.googleapis.com/index.html
# comparing tools/CURRENT_RELEASE to LATEST_RELEASE to know if it is the latest
import sys
import os
import zipfile
import requests

latest_url = 'http://chromedriver.storage.googleapis.com/LATEST_RELEASE'
latest_release = requests.get(latest_url, timeout=5).text.strip()

ROOT_PATH = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'pisces')

# rewrite CURRENT_RELEASE to newest
current_file = os.path.join(ROOT_PATH, 'tools', 'CURRENT_RELEASE')
with open(current_file, 'w') as f_write:
    f_write.write(latest_release)


def decide_platform(mode='auto', platform=None):
    if mode == 'auto':
        platform = platform or sys.platform
        if platform == 'darwin':
            origin_url = 'http://chromedriver.storage.googleapis.com/{}/chromedriver_mac64.zip'.format(latest_release)
            chromedriver = os.path.join(ROOT_PATH, 'tools', 'chromedriver_mac')
            unzip_file = os.path.join(ROOT_PATH, 'tools', 'chromedriver')
        elif platform == 'linux':
            origin_url = 'http://chromedriver.storage.googleapis.com/{}/chromedriver_linux64.zip'.format(latest_release)
            chromedriver = os.path.join(ROOT_PATH, 'tools', 'chromedriver_linux')
            unzip_file = os.path.join(ROOT_PATH, 'tools', 'chromedriver')
        elif platform in ['win32', 'cygwin']:
            origin_url = 'http://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip'.format(latest_release)
            chromedriver = os.path.join(ROOT_PATH, 'tools', 'chromedriver.exe')
            unzip_file = os.path.join(ROOT_PATH, 'tools', 'chromedriver.exe')
        else:
            raise AssertionError('%s is not supported' % platform)
        return [[origin_url, unzip_file, chromedriver], ]
    elif mode == 'all':
        ret_list = []
        for p in ['darwin', 'linux', 'win32']:
            ret_list.extend(decide_platform(mode='auto', platform=p))
        return ret_list


def update(origin_url, unzip_file, chromedriver):
    # download zip_file
    print("download %s to %s" % (origin_url, chromedriver))
    zip_file = os.path.join(ROOT_PATH, 'tools', os.path.basename(origin_url))
    r = requests.get(origin_url, stream=True, timeout=10)
    with open(zip_file, 'wb') as f_write:
        for chunk in r.iter_content(1024 * 1024):
            f_write.write(chunk)

    # unzip zip_file
    with zipfile.ZipFile(zip_file, 'r') as read_zip:
        read_zip.extractall(os.path.join(ROOT_PATH, 'tools'))

    # delete zip_file
    if os.path.exists(zip_file):
        os.remove(zip_file)

    # rename unzip_file
    os.chmod(unzip_file, 0o755)
    if unzip_file != chromedriver:
        os.rename(unzip_file, chromedriver)

if __name__ == "__main__":
    _mode = sys.argv[1] if len(sys.argv) >= 2 else 'auto'
    if _mode not in ['auto', 'all']:
        print("usage: python scripts/update_chromedriver.py [all/auto]")
        sys.exit(1)
    for origin_url, unzip_file, chromedriver in decide_platform(_mode):
        update(origin_url, unzip_file, chromedriver)
