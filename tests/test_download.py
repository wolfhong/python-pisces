# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import shutil
from pisces import Pisces

# make user you can use google/bing/yahoo/sogou/baidu/360 search engine


def test_download_by_word():
    test_name = 'output_test'
    if os.path.exists(test_name):
        shutil.rmtree(test_name)

    keyword = '火灾'
    # engine_list = ['baidu', '360', 'sogou', 'yahoo', 'google', 'bing', ]
    engine_list = ['baidu', 'yahoo', 'google', 'bing', ]
    with Pisces() as client:
        image_count = 2
        for engine in engine_list:
            print("test %s ..." % engine)
            output_dir = os.path.join(test_name, engine)
            ret = client.download_by_word(keyword, output_dir, engine=engine, image_count=image_count)
            assert ret == image_count
            assert len(os.listdir(output_dir)) == image_count

    if os.path.exists(test_name):
        shutil.rmtree(test_name)
