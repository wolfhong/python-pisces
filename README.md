[![PyPI](https://img.shields.io/pypi/v/python-pisces.svg)](https://pypi.python.org/pypi/python-pisces)

## Why use pisces?

This project origins from the needs of image dataset for algorithm training.

Image search engines, such as Google, are quite powerful now. They are enough if we could use them.
However, they didn't provide convenient API for us.

Pisces uses [selenuim](https://www.seleniumhq.org/), which can work with chromedriver to download the images we need.
Pisces supports these search engines: google, yahoo, bing, baidu(china) and more mainstream engines in the future.

## Why use pisces?(Chinese)

本项目起源于算法训练需要图像数据集的需求.

现有的图片搜索引擎,比如Google,相当强大了,能够利用起来,已经可以满足我们的需求. 然而,这些网站并没有提供方便的API让我们得到图片链接.

Pisces使用了[selenuim](https://www.seleniumhq.org/), 可调用主流的浏览器下载搜索到的图片. Pisces还整合了其他的搜索引擎的搜索结果:google/yahoo/bing/百度.

## Installation

First, make sure you have [chrome](https://www.google.com/chrome/) browser installed on your computer.
If not, selenium gives "selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary".

If you're working on a server without interface (for example, CentOS), you can also follow the steps below to install it:

    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
    yum -y localinstall google-chrome-stable_current_x86_64.rpm

Use pip:

    pip install python-pisces

From source code:

    git clone https://github.com/wolfhong/python-pisces.git
    cd python-pisces

    pip install -r requirements.txt
    export PYTHONPATH=./
    python scripts/update_chromedriver.py  # download newest chromedriver according to platform
    python setup.py install

In addition to chrome, you can also use [firefox](https://www.mozilla.org/). However, you need to do extra settings for firefox. You have to download [geckodriver](https://github.com/mozilla/geckodriver/releases) and put it into your `$PATH`, which helps selenium interacting with firefox browser.

Pisces uses chrome as the default browser. You needn't download [chromedriver](http://chromedriver.storage.googleapis.com/index.html) youself because Pisces has built-in ones.

Pisces first finds chromedriver (for Chrome) or geckodriver (for Firefox) in `pisces/tools/` in its package. If not, then finds it in `$PATH`.

## Console Command

Once you have installed Pisces, you can easily use it to search for and download images by keywords:

    $ pisces -e google -w 8 -n 500 fire "kitchen fire" -o ./output

The above command will start up chromedriver and then google "fire" and "kitchen fire" with its image search engine,
download images with 8 threads parallelly and then restore these images in "./output" directory.

If you're in China, you're recommended to use `-e baidu` instand of `-e google`(default), because of some network problems. (在中国由于一些网络原因，推荐使用参数`-e baidu`，而不是默认的`-e google`)

![image](https://raw.githubusercontent.com/wolfhong/python-pisces/develop/overview.png)

Use `pisces -h` to show the usage:

``` console
    usage: command.py [-h] [-q] [--display] [-e ENGINE] [-w WORKERS] [-n NUMBER]
                  [-o OUTPUT_DIR] [-v]
                  [keywords [keywords ...]]

    Use keywords to search for and download images.

    positional arguments:
      keywords              keywords to search for images

    optional arguments:
      -h, --help            show this help message and exit
      -q, --quiet           quiet (no output)
      --display             start up browser with a graphical display, default to no
      -e ENGINE, --engine ENGINE
                            the image search engine you want to use, default to
                            google. select within [google, bing, yahoo, baidu]
      -b BROWSER, --browser BROWSER
                            the browser you have installed, default to chrome.
                            select within [chrome, firefox]
      -w WORKERS, --workers WORKERS
                            the number of threads when downloading images, default
                            to cpu core count
      -n NUMBER, --number NUMBER
                            the max number of images you want to download, default
                            to 100
      -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            destination to store downloaded images, default to
                            ./output
      -v, --version         print the version and exit
```

Pisces can work on these platforms: windows, linux, mac, and it had beed tested.
If not, you're welcome to [file an issue](https://github.com/wolfhong/python-pisces/issues).

More examples:
    
``` console
    $ pisces "kitchen fire" "forest fire"
    $ pisces -n500 "厨房火灾" "森林火灾"
    $ pisces -e baidu -n500 -o path-to-output 火灾 水灾
```

## Code Example

Pisces can also be included in your projects:

``` python
    from pisces import Pisces

    # recommended to use `with`:
    with Pisces(quiet=False, headless=False) as client:
        output_dir = './output_water/'
        client.download_by_word('water', output_dir, engine='google', image_count=20)

    # or call `close()` handly:
    client = Pisces(quiet=False, headless=True, workers=4, browser='chrome')
    output_dir = './output_fire/'
    client.download_by_word('fire', output_dir, engine='baidu', image_count=20)
    client.close()
```

## Tips

- The code uses selenuim. More info to see [ReadTheDocs](http://selenium-python.readthedocs.io/installation.html)
- If you're in China, you're recommended to use `-e baidu` instand of `-e google`(default), because of some network problems.

## About

Pisces is just a tools to search for and download images by keywords, using image search engine such as google, bing, baidu, etc.
I hope it could help you in somewhere.

* [Issue tracker](https://github.com/wolfhong/python-pisces/issues?status=new&status=open)
* [Source Code](https://github.com/wolfhong/python-pisces)
* [PyPI](https://pypi.python.org/pypi/python-pisces)
