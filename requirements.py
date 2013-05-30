# -*- coding: utf-8 -*-

""" Requirements generator. """

from csv import DictReader
from os import remove, makedirs
from os.path import exists, join

from pandoc import md_to_pdf_with_template

f = open('templates/md/req/requirement_table.md', 'r')
requirement_table_template = f.read()
f.close()

f = open('templates/md/req/introduction.md', 'r')
introduction_template = f.read()
f.close()


def process_requirement(requirement, md_file):
    """  Process requirement into Markdown format. """
    requirement_id = int(requirement['ID'])
    if requirement_id % 100 == 0:
        md_file.write('### {}\n'.format(requirement['Name/Title']))
    else:
        md_file.write(requirement_table_template.format(**requirement))
    md_file.write('\n')


def import_csv(input_file, md_file):
    """ Imports the CSV file into Markdown format. """

    with open(input_file, 'rb') as csv_file:
        content = DictReader(csv_file, delimiter=',')
        for requirement in content:
            process_requirement(requirement, md_file)


def create_header(md_file):
    """ Creates the header document in Markdown format. """

    context = {
        'project_title': raw_input('Project title: '),
        "client_name": raw_input('Client name: '),
    }

    md_file.write(introduction_template.format(**context))

    return context


def tmp_cleanup():
    """ Removes generated tmp files. """

    remove('.tmp.md')


def requirements_generator(input_file, output_folder='output'):
    # md output file
    with open('.tmp.md', 'w') as md_file:
        # header creation
        context = create_header(md_file)

        # import csv into md
        import_csv(input_file, md_file)

    # output to PDF
    if not exists(output_folder):
        makedirs(output_folder)
    md_file = '.tmp.md'
    pdf_file = '{}.pdf'.format(context['project_title'])
    pdf_file = join(output_folder, pdf_file)
    template = 'templates/requirements.tex'
    md_to_pdf_with_template(md_file, pdf_file, template)

    # tmp files cleanup
    tmp_cleanup()
