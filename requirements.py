# -*- coding: utf-8 -*-

""" Requirements generator. """

from csv import DictReader
from os import remove, makedirs
from os.path import exists, join

from pandoc import md_to_pdf_with_template


def process_requirement(requirement, md_file):
    """  Process requirement into Markdown format. """

    md_file.write('### Requerimiento ID: {}\n'.format(requirement['ID']))
    md_file.write('* Nombre: {}\n'.format(requirement['Name/Title']))
    md_file.write('* Descripción: {}\n'.format(requirement['Description']))
    md_file.write('\n')


def import_csv(input_file, md_file):
    """ Imports the CSV file into Markdown format. """

    with open(input_file, 'rb') as csv_file:
        content = DictReader(csv_file, delimiter=',')
        for requirement in content:
            process_requirement(requirement, md_file)


def create_header(md_file):
    """ Creates the header document in Markdown format. """

    project_title = raw_input('Project title: ')
    md_file.write('# Proyecto {}\n'.format(project_title))
    client_name = raw_input('Client name: ')
    md_file.write('## Cliente: {}\n\n'.format(client_name))

    return project_title


def tmp_cleanup():
    """ Removes generated tmp files. """

    remove('.tmp.md')


def requirements_generator(input_file, output_folder='output'):
    # md output file
    with open('.tmp.md', 'w') as md_file:
        # header creation
        project_title = create_header(md_file)

        # import csv into md
        import_csv(input_file, md_file)

    # output to PDF
    if not exists(output_folder):
        makedirs(output_folder)
    md_file = '.tmp.md'
    pdf_file = '{}.pdf'.format(project_title)
    pdf_file = join(output_folder, pdf_file)
    template = 'templates/requirements.tex'
    md_to_pdf_with_template(md_file, pdf_file, template)

    # tmp files cleanup
    tmp_cleanup()
