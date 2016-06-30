#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="pisces",
    version="0.10",
    license="MIT",
    description="image crawler for image search engines: google/baidu/yahoo/bing/sogou/360",
    author="wolfhong",
    author_email="hongxucai1991@163.com",
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests>=2.2.1',
        'selenium==2.53.6',
    ],
)
