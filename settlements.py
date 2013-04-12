# -*- coding: utf-8 -*-

""" Settlements generator. """

from zipfile import ZipFile
from os.path import exists
from os import makedirs, listdir
from os.path import splitext, join

from pandoc import md_to_pdf_with_template


def settlements_generator(settlements_package, tmp_folder='tmp',
                          output_folder='output'):
    """ Generates settlements. """

    settlements = ZipFile(settlements_package)
    if not exists(tmp_folder):
        makedirs(tmp_folder)
    if not exists(output_folder):
        makedirs(output_folder)

    settlements.extractall(tmp_folder)
    for settlement in listdir(tmp_folder):
        md_file = join(tmp_folder, settlement)
        pdf_file = '{}.pdf'.format(splitext(settlement)[0])
        pdf_file = join(output_folder, pdf_file)
        template = 'templates/wage_settlement.tex'
        md_to_pdf_with_template(md_file, pdf_file, template)

    settlements.close()
