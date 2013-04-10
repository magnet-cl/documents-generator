#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Requirements Generator.

Usage:
    generate.py <input.csv>
    generate.py (-h | --help)
    generate.py --version


Options:
    -h --help   Show this screen.
    --version   Show version.

"""

from docopt import docopt
from csv import DictReader
from os.path import exists
from os import remove

from pandoc import md_to_latex
from pandoc import latex_to_pdf


def process_requirement(requirement, md_file):
    """  Process requirement into Markdown format. """

    md_file.write('## Requerimiento ID: {}\n'.format(requirement['ID']))
    md_file.write('* Nombre: {}\n'.format(requirement['Name/Title']))
    md_file.write('* Descripción: {}\n'.format(requirement['Description']))
    md_file.write('* Fecha de Inicio: {}\n'.format(requirement['Start Date']))
    md_file.write('* Fecha de Término: {}\n'.format(requirement['End Date']))
    md_file.write('\n')


def import_csv(input_file, md_file):
    """ Imports the CSV file into Markdown format. """

    with open(input_file, 'rb') as csv_file:
        content = DictReader(csv_file, delimiter=',')
        print content.fieldnames
        for requirement in content:
            process_requirement(requirement, md_file)


def create_header(md_file):
    """ Creates the header document in Markdown format. """

    project_title = raw_input('Project title: ')
    md_file.write('# Proyecto {}\n'.format(project_title))
    client_name = raw_input('Client name: ')
    md_file.write('## Cliente: {}\n'.format(client_name))


def tmp_cleanup():
    """ Removes generated tmp files. """

    remove('.tmp.md')
    remove('.tmp.tex')


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Requirements Generator 0.1')

    input_file = arguments['<input.csv>']

    if exists(arguments['<input.csv>']):
        print("Processing file: {}".format(input_file))
        # md output file
        with open('.tmp.md', 'w') as md_file:
            # header creation
            create_header(md_file)

            # import csv into md
            import_csv(input_file, md_file)

        # output to LaTeX and PDF
        md_to_latex()
        latex_to_pdf()

        # tmp files cleanup
        tmp_cleanup()

    else:
        print("{}: File not found.".format(input_file))
