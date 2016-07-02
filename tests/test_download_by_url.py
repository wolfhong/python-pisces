# -*- coding: utf-8 -*-
import sys
import os
add_path = os.path.abspath(os.path.dirname(__file__))  # tests
add_path = os.path.abspath(os.path.dirname(add_path))  # bin
sys.path.insert(0, add_path)

from pisces import Pisces


def test_download_by_url():
    # 使用关键词 "火灾" 进行测试
    baidu_url = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E7%81%AB%E7%81%BE'
    so_url = 'http://image.so.com/i?q=%E7%81%AB%E7%81%BE&src=srp'
    sogou_url = 'http://pic.sogou.com/pics?query=%BB%F0%D4%D6&di=2&_asf=pic.sogou.com&w=05009900&sut=452&sst0=1467201379776'
    yahoo_url = 'https://sg.images.search.yahoo.com/search/images;_ylt=A2oKiHLOvXRXqxMA4ckl4gt.;_ylu=X3oDMTBsZ29xY3ZzBHNlYwNzZWFyY2gEc2xrA2J1dHRvbg--?p=%E7%81%AB%E7%81%BE&fr=sfp&fr2=p%3As%2Cv%3Ai%2Cm%3Asb-top&ei=UTF-8&n=60&x=wrt&y=Search'
    bing_url = 'http://www.bing.com/images/search?q=kitchen+fire&qpvt=kitchen+fire&qpvt=kitchen+fire&qpvt=kitchen+fire&FORM=IGRE'
    google_url = 'https://www.google.com/search?safe=strict&hl=zh-CN&site=imghp&tbm=isch&source=hp&biw=1372&bih=661&q=%E7%81%AB%E7%81%BE&oq=%E7%81%AB%E7%81%BE&gs_l=img.3...1527.6030.0.6271.25.13.7.0.0.0.333.333.3-1.1.0....0...1ac.1j4.64.img..18.7.33...0.m7j-m12CPV0'

    tuple_list = [
        ('baidu', baidu_url),
        ('360', so_url),
        ('sogou', sogou_url),
        ('yahoo', yahoo_url),
        ('bing', bing_url),
        ('google', google_url),
    ]
    client = Pisces(close=True, quiet=True, browser='firefox')
    for engine, url in tuple_list:
        image_count = 1
        output_dir = os.path.join(add_path, 'output_test', engine)
        ret = client.download_by_url(url, output_dir, image_count=image_count)
        if ret == image_count:
            print '%s ok...' % engine
        else:
            print '%s error!!!' % engine

test_download_by_url()
