#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Magnet documents generator.

Usage:
    generate.py req <input.csv>
    generate.py settlements <dir>
    generate.py (-h | --help)
    generate.py --version


Options:
    -h --help   Show this screen.
    --version   Show version.

"""

from docopt import docopt
from os.path import exists

from requirements import requirements_generator
from settlements import settlements_generator


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Requirements Generator 0.1')

    if arguments['req']:
        input_file = arguments['<input.csv>']

        if exists(arguments['<input.csv>']):
            print("Processing file: {}".format(input_file))
            requirements_generator(input_file)
        else:
            print("{}: File not found.".format(input_file))

    elif arguments['settlements']:
        settlements_dir = arguments['<dir>']
        if exists(settlements_dir):
            print("Processing directory: {}".format(settlements_dir))
            settlements_generator(settlements_dir)
        else:
            print("{}: Directory not found".format(settlements_dir))
