# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
from argparse import ArgumentParser
from pisces import __version__, Pisces

unicode_type = unicode if sys.version_info[0] == 2 else str


def create_parser():
    parser = ArgumentParser(description="Using keywords to search for and download images.")
    parser.add_argument('-q', '--quiet',
                        action="store_true",
                        default=False,
                        help="quiet(no output)")
    parser.add_argument('-e', '--engine',
                        action="store",
                        default="google",
                        choices=["google", "bing", "yahoo", "baidu", "sougou", "360"],
                        help="image search engine you want to use, default to google")
    parser.add_argument('-w', '--workers',
                        action="store",
                        default=0,
                        type=int,
                        help="the number of threads when downloading images, default to the cpu count")
    parser.add_argument('-n', '--number',
                        action="store",
                        default=200,
                        type=int,
                        help="the max number of images you want to download, default to 200")
    parser.add_argument('-o', '--output_dir',
                        action="store",
                        default='./output',
                        help="destination to store downloaded images, default to ./output"
                        )
    parser.add_argument('keywords',
                        action="store",
                        nargs='*',
                        help="keywords to search images")
    parser.add_argument('-v', '--version',
                        action="store_true",
                        default=False,
                        help="print the version and exit")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        sys.stdout.write(__version__ + os.linesep)
        sys.exit(0)
    keywords = args.keywords
    if not keywords:
        parser.print_help()
        sys.exit(1)
    for i, word in enumerate(keywords):
        if not isinstance(word, unicode_type):
            keywords[i] = word.decode(sys.stdin.encoding)
    with Pisces(quiet=args.quiet, workers=args.workers) as client:
        for word in keywords:
            output_dir = os.path.join(args.output_dir, word)
            client.download_by_word(word, args.engine, output_dir, image_count=args.number)
    sys.exit(0)

if __name__ == '__main__':
    main()
