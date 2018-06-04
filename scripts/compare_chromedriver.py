#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tools/chromedriver is downloaded from http://chromedriver.storage.googleapis.com/index.html
# comparing tools/CURRENT_VERSION to LATEST_RELEASE to know if it is the latest
import sys
import os

PY3 = sys.version_info[0] == 3
if PY3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

latest_url = 'http://chromedriver.storage.googleapis.com/LATEST_RELEASE'
latest_release = urlopen(latest_url).read().strip()

current_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools', 'CURRENT_RELEASE')
with open(current_file) as f_read:
    current_release = f_read.read().strip()

print('latest version: {}'.format(latest_release))
print('current version: {}'.format(current_release))
if latest_release != current_release:
    print('download latest release from {}'.format(latest_url))
