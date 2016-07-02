# -*- coding: utf-8 -*-
import sys
import os
add_path = os.path.abspath(os.path.dirname(__file__))  # tests
add_path = os.path.abspath(os.path.dirname(add_path))  # bin
sys.path.insert(0, add_path)

from pisces import Pisces


def test_download_by_word():
    # 使用关键词 "火灾" 进行测试
    keyword = u'火灾'
    engine_list = ['baidu', '360', 'sogou', 'yahoo', 'bing', 'google', ]
    client = Pisces(close=True, quiet=True, browser='firefox')
    for engine in engine_list:
        image_count = 1
        output_dir = os.path.join(add_path, 'output_test', engine)
        ret = client.download_by_word(keyword, engine, output_dir, image_count=image_count)
        if ret == image_count:
            print '%s ok...' % engine
        else:
            print '%s error!!!' % engine

test_download_by_word()
