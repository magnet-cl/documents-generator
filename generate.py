#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Magnet documents generator.

Usage:
    generate.py req <client_name> [<input.csv>]
    generate.py settlements <package.tar.gz>
    generate.py (-h | --help)
    generate.py --version


Options:
    -h --help   Show this screen.
    --version   Show version.

"""

from docopt import docopt
from os.path import exists
from os import makedirs
from sys import exit

from requirements import RequirementsGenerator
from settlements import settlements_generator

import shutil

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Requirements Generator 0.2')

    if arguments['req']:
        client_name = arguments['<client_name>']
        client_folder = 'clients/%s' % client_name

        if not exists(client_folder):
            makedirs(client_folder)

        input_csv = arguments['<input.csv>']
        input_file = "%s/input.csv" % client_folder

        if not input_csv:
            if not exists(input_file):
                print ("You must provide an input file if this is the first "
                       "time you run this script")
                exit()
            print("Processing file: {}".format(input_file))

        elif exists(input_csv):
            print input_csv, input_file
            shutil.copy2(input_csv, input_file)
            print("Processing file: {}".format(input_csv))
        else:
            print("{}: File not found.".format(input_csv))
            exit()

        requirements_generator = RequirementsGenerator()
        requirements_generator.generate(input_file)

    elif arguments['settlements']:
        settlements_package = arguments['<package.tar.gz>']
        if exists(settlements_package):
            print("Processing compressed file: {}".format(settlements_package))
            settlements_generator(settlements_package)
        else:
            print("{}: File not found".format(settlements_package))
