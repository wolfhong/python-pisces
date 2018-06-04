# -*- coding: utf-8 -*-
from argparse import ArgumentParser


def create_parse():
    parser = ArgumentParser(description="Find and download images by words")
    parser.add_argument('-s', '--simple',
                        action="store_true",
                        default=False,
                        help="only show explainations. "
                             "argument \"-f\" will not take effect.")
    parser.add_argument('-S', '--speech',
                        action="store_true",
                        default=False,
                        help="print URL to speech audio.")
    parser.add_argument('-r', '--read',
                        action="store_true",
                        default=False,
                        help="read out the word with player provided by \"-p\" option.")
    parser.add_argument('-p', '--player',
                        choices=['festival', 'mpg123', 'sox', 'mpv'],
                        default='festival',
                        help="read out the word with this play."
                             "Default to 'festival' or can be 'mpg123', 'sox', 'mpv'."
                             "-S option is required if player is not festival."
                        )
    parser.add_argument('-a', '--accent',
                        choices=['auto', 'uk', 'us'],
                        default='auto',
                        help="set default accent to read the word in. "
                             "Default to 'auto' or can be 'uk', or 'us'."
                        )
    parser.add_argument('-x', '--selection',
                        action="store_true",
                        default=False,
                        help="show explaination of current selection.")
    parser.add_argument('--color',
                        choices=['always', 'auto', 'never'],
                        default='auto',
                        help="colorize the output. "
                             "Default to 'auto' or can be 'never' or 'always'.")
    parser.add_argument('words',
                        nargs='*',
                        help="words to lookup, or quoted sentences to translate.")
    return parser.parse_args()
