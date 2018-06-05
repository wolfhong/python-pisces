[![PyPI](https://img.shields.io/pypi/v/pisces-image.svg)](https://pypi.python.org/pypi/pisces-image)

## Why use pisces?

This project origins from the needs of image dataset for algorithm training.

Image search engines, such as Google, are quite powerful now. It's enough if we could use it.
However, it doesn't provide convenient API for us.

Pisces uses selenuim, which can work with the mainstream browsers to download the images we need.
Pisces supports these search engines: google, yahoo, bing, baidu(china), sogou(china), 360(china), and more in the future.

本项目起源于算法训练需要图像数据集的需求.

现有的图片搜索引擎,比如Google,相当强大了,能够利用起来,已经可以满足我们的需求.然而,这些网站并没有提供方便的API让我们得到图片链接.

Pisces使用了selenuim,可调用主流的浏览器下载搜索到的图片.Pisces还整合了其他的搜索引擎的搜索结果:google/yahoo/bing/百度/sogou/360,丰富可采集的数据集.

## Installation

Use pip:

    pip install pisces-image


## Console Command

Once you have installed Pisces, you can easily use it to search for and download images:

    $ pisces -e google --display -w 8 -n 500 fire "kitchen fire" -o ./output

The above command will start up chromedriver and then google "fire" and "kitchen fire" with its image search engine,
download images with 8 threads parallelly and then restore these images in "./output" directory.

If you're in China, you're recommended to use `-e baidu` instand of `-e google`(default), because of some network problems. (在中国由于一些网络原因，推荐使用参数`-e baidu`，而不是默认的`-e google`)

![image](./output-overview.png)

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
      --display             work with a graphical display
      -e ENGINE, --engine ENGINE
                            the image search engine you want to use, default to
                            google. select within [google, bing, yahoo, baidu,
                            sougou, 360]
      -w WORKERS, --workers WORKERS
                            the number of threads when downloading images, default
                            to the cpu count
      -n NUMBER, --number NUMBER
                            the max number of images you want to download, default
                            to 100
      -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            destination to store downloaded images, default to
                            ./output
      -v, --version         print the version and exit
```

`pisces` console command can work on any platform: windows, linux, mac, and it had beed fully tested.
If not, you're welcome to [file an issue](https://github.com/wolfhong/pisces/issues).

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
    client = Pisces(quiet=False, headless=True, workers=4)
    output_dir = './output_fire/'
    client.download_by_word('fire', output_dir, engine='baidu', image_count=20)
    client.close()
```

## Tips

- The code uses selenuim. More info to see [ReadTheDocs](http://selenium-python.readthedocs.io/installation.html)
- If you're in China, you're recommended to use `-e baidu` instand of `-e google`(default), because of some network problems.

## About

Pisces is just a tools to search for and download images, using image search engine such as google, bing, baidu, etc.
I hope it can help you in somewhere.

* [Issue tracker](https://github.com/wolfhong/pisces/issues?status=new&status=open)
* [Current Source on GitHub](https://github.com/wolfhong/pisces)
* [PyPI](https://pypi.python.org/pypi/pisces-image)
