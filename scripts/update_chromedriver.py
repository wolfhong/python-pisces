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

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# rewrite CURRENT_RELEASE to newest
current_file = os.path.join(ROOT_PATH, 'tools', 'CURRENT_RELEASE')
with open(current_file, 'w') as f_write:
    f_write.write(latest_release)


if sys.platform == 'darwin':
    origin_url = 'http://chromedriver.storage.googleapis.com/{}/chromedriver_mac64.zip'.format(latest_release)
    CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools', 'chromedriver_mac')
    unzip_file = os.path.join(ROOT_PATH, 'tools', 'chromedriver')
elif sys.platform == 'linux':
    origin_url = 'http://chromedriver.storage.googleapis.com/{}/chromedriver_linux64.zip'.format(latest_release)
    CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools', 'chromedriver_linux')
    unzip_file = os.path.join(ROOT_PATH, 'tools', 'chromedriver')
elif sys.platform in ['win32', 'cygwin']:
    origin_url = 'http://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip'.format(latest_release)
    CHROMEDRIVER = os.path.join(ROOT_PATH, 'tools', 'chromedriver.exe')
    unzip_file = os.path.join(ROOT_PATH, 'tools', 'chromedriver.exe')
else:
    raise AssertionError('%s is not supported' % sys.platform)


# download zip_file
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
if unzip_file != CHROMEDRIVER:
    os.rename(unzip_file, CHROMEDRIVER)
