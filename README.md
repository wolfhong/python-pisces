## Why use pisces?
The project origins from the needs of image data-set for algorithm training.

Image search engines, such as Google, are quite powerful now. It's enough if we can use them. However, these sites don't provide convenient API for us.

Pisces uses selenuim, which can work with the mainstream browsers to download the images we need. Pisces incorporates the search engines: google, yahoo, bing, Baidu, sogou, 360, and more in the future.

本项目起源于算法训练需要图像数据集的需求.

现有的图片搜索引擎,比如Google,相当强大了,能够利用起来,已经可以满足我们的需求.然而,这些网站并没有提供方便的API让我们得到图片链接.

pisces使用了selenuim,可调用主流的浏览器下载搜索到的图片.pisces还整合了其他的搜索引擎的搜索结果:google/yahoo/bing/百度/sogou/360,丰富可采集的数据集.

## Installation
- clone the code and enter the folder
- python install setup.py
- or you can directly place the pisces into your project.


## Example

    # -*- coding: utf-8 -*-
    from pisces import Pisces

    if __name__ == '__main__':
        # image search keyword: kitchen fire
        url = 'https://www.google.com/search?safe=strict&hl=zh-CN&site=imghp&tbm=isch&source=hp&biw=1372&bih=661&q=%E7%81%AB%E7%81%BE&oq=%E7%81%AB%E7%81%BE&gs_l=img.3...1527.6030.0.6271.25.13.7.0.0.0.333.333.3-1.1.0....0...1ac.1j4.64.img..18.7.33...0.m7j-m12CPV0'
        # if you are in china, use the url below instand.
        # url = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E7%81%AB%E7%81%BE'

        output_dir = '/tmp/output_fire/'
        client = Pisces(quiet=False, close=True, browser='firefox')
        # similar to: client = Pisces()
        client.download_by_url(url, output_dir, image_count=100)

        output_dir = '/tmp/output_water/'
        # use google to download image with keyword: water
        client.download_by_word('water', 'google', output_dir, image_count=100)


## Tip
- The code uses selenuim. Selenium Python bindings provides a simple API to write functional/acceptance tests using Selenium WebDriver. More info to see http://selenium-python.readthedocs.io/installation.html
- default browser is firefox;
- tools/chromedriver is only for chrome, to see http://chromedriver.storage.googleapis.com/index.html for more info.
- browser safari/IE/opera may not work if you don't have any support
- I recommend to use the default browser - firefox.
