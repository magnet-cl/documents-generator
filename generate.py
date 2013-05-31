#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Magnet documents generator.

Usage:
    generate.py req <input.csv>
    generate.py settlements <package.tar.gz>
    generate.py (-h | --help)
    generate.py --version


Options:
    -h --help   Show this screen.
    --version   Show version.

"""

from docopt import docopt
from os.path import exists

from requirements import RequirementsGenerator
from settlements import settlements_generator


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Requirements Generator 0.1')

    if arguments['req']:
        input_file = arguments['<input.csv>']

        if exists(arguments['<input.csv>']):
            print("Processing file: {}".format(input_file))
            requirements_generator = RequirementsGenerator()
            requirements_generator.generate(input_file)
        else:
            print("{}: File not found.".format(input_file))

    elif arguments['settlements']:
        settlements_package = arguments['<package.tar.gz>']
        if exists(settlements_package):
            print("Processing compressed file: {}".format(settlements_package))
            settlements_generator(settlements_package)
        else:
            print("{}: File not found".format(settlements_package))
