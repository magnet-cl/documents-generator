# -*- coding: utf-8 -*-

""" Requirements generator. """

from csv import DictReader
from os import remove, makedirs
from os.path import exists, join
from shutil import copy2
from datetime import date, datetime, timedelta
from pandoc import md_to_pdf_with_template
from requirements.config import RequirementsConfigParser
from requirements import utils

import csv


class RequirementsGenerator():
    colors = ["grey1", "blue2", "green1", "purple1", "red1", "orange1",
              "blue1", "yellow1"]

    holidays = (
        date(2014, 01, 01), date(2014, 04, 18), date(2014, 4, 19),
        date(2014, 05, 01), date(2014, 05, 21), date(2014, 5, 29),
        date(2014, 07, 16), date(2014, 8, 15), date(2014, 9, 18),
        date(2014, 9, 19), date(2014, 10, 12), date(2014, 10, 31),
        date(2014, 11, 01), date(2014, 12, 8), date(2014, 12, 25)
    )

    def __init__(self, context):
        self.initialize()

        self.context = context
        self.pdf_title = "Requerimientos"

    def set_templates(self):
        client_name = self.context['client_name']

        client_folder = utils.project_path(self.context)

        template_folder = '%s/templates/md/' % client_folder
        if not client_name or not exists(template_folder):
            makedirs(template_folder)
            source_folder = 'templates/md/req/%s'
            copy2(source_folder % 'introduction.md', template_folder)
            copy2(source_folder % 'requirement_table.md', template_folder)
            copy2(source_folder % 'non_functional_title.md', template_folder)

        template_folder += "%s"

        f = open(template_folder % 'requirement_table.md', 'r')
        self.requirement_table_template = f.read()
        f.close()

        f = open(template_folder % 'introduction.md', 'r')
        self.introduction_template = f.read()
        f.close()

        f = open(template_folder % 'non_functional_title.md', 'r')
        self.non_functional_title_template = f.read()
        f.close()

    def initialize(self):
        self.current_group_name = ""
        self.accumulated_hours = 0
        self.start_date = None
        self.color_index = 0

    def process_requirement(self, requirement, md_file):
        """  Process requirement into Markdown format. """
        try:
            requirement_id = int(requirement['ID'])
        except:
            return

        description = requirement['Description']
        if not description:
            return

        if requirement_id % 100 == 0:
            if requirement_id == 1000:
                md_file.write(self.non_functional_title_template.format(
                    **self.context
                ))
            md_file.write('### {}\n'.format(requirement['Name/Title']))
            md_file.write('%s\n' % description)
        else:
            md_file.write(
                self.requirement_table_template.format(**requirement))

        md_file.write('\n')

    def import_csv(self, input_file, md_file):
        """ Imports the CSV file into Markdown format. """

        with open(input_file, 'rb') as csv_file:
            content = DictReader(csv_file, delimiter=',')

            self.set_templates()
            self.create_header(md_file)

            for requirement in content:
                self.process_requirement(requirement, md_file)

    def reformat_requirement(self, requirement, csv_file):
        """ Creates a new row, using the specified requirement dict """
        try:
            requirement_id = int(requirement['ID'])
        except:
            return
        if requirement_id == 0:
            return

        description = requirement['Description']
        if not description:
            return

        if requirement_id % 100 == 0:
            self.current_group_name = requirement['Name/Title']
            self.color_index += 1
            self.color_index %= len(self.colors)
            return

        line = [self.current_group_name, requirement['Name/Title'],
                '"%s"' % description]

        hh = int(requirement['HH'])

        # calculate the start_date
        days = self.accumulated_hours / 8
        start_date = self.start_date + timedelta(days=days)

        week_day = start_date.weekday()
        if week_day == 5 or week_day == 6:
            delta = 7 - week_day
            start_date = start_date + timedelta(days=delta)
            self.accumulated_hours += 8 * delta

        while start_date in self.holidays:
            start_date = start_date + timedelta(days=1)
            self.accumulated_hours += 8

        line.append(start_date.isoformat())

        self.accumulated_hours += hh

        days = self.accumulated_hours / 8

        if self.accumulated_hours % 8 == 0:
            days = days - 1

        end_date = self.start_date + timedelta(days=days)
        week_day = end_date.weekday()
        if week_day == 5 or week_day == 6:
            delta = 7 - week_day
            end_date = end_date + timedelta(days=delta)

        while start_date in self.holidays:
            start_date = start_date + timedelta(days=1)
            self.accumulated_hours += 8

        line.append(end_date.isoformat())

        line.append(self.colors[self.color_index])

        self.scv_writer.writerow(line)

    def reformat_csv(self, input_file, csv_file):
        """ Creates a new csv file to be imported to team_gantt """

        with open(input_file, 'rb') as input_csv_file:
            # write the first headers
            self.scv_writer = csv.writer(
                csv_file, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL)

            self.scv_writer.writerow(['Group', 'Name/Title', 'Notes',
                                      'Start Date', 'End Date', 'Color'])

            content = DictReader(input_csv_file, delimiter=',')
            for requirement in content:
                self.reformat_requirement(requirement, csv_file)

    def create_header(self, md_file):
        """ Creates the header document in Markdown format. """

        md_file.write(self.introduction_template.format(**self.context))

    def tmp_cleanup(self):
        """ Removes generated tmp files. """

        remove('.tmp.md')

    def generate_requirements(self, input_file):
        # md output file
        with open('.tmp.md', 'w') as md_file:
            # import csv into md
            self.import_csv(input_file, md_file)

        output_folder = '%s/output' % utils.project_path(self.context)
        print output_folder

        # output to PDF
        if not exists(output_folder):
            makedirs(output_folder)

        md_file = '.tmp.md'
        pdf_file = 'Requerimientos {}.pdf'.format(self.context['client_name'])
        pdf_file = join(output_folder, pdf_file)
        template = 'templates/requirements.tex'
        md_to_pdf_with_template(md_file, pdf_file, template)

        # tmp files cleanup
        self.tmp_cleanup()

    def generate_gantt(self, input_file):
        output_folder = '%s/output' % utils.project_path(self.context)

        # tmp files cleanup
        self.tmp_cleanup()

        config = RequirementsConfigParser(self.context)

        stored_date = config.get('Gantt', 'start_date')
        if stored_date:
            message = ('Start date (%s) (leave blank for %s): ' %
                       ('%Y-%m-%d', stored_date))
        else:
            message = 'Start date (%Y-%m-%d)(leave blank for today): '

        raw_date = raw_input(message)

        if raw_date:
            self.start_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        elif stored_date:
            self.start_date = datetime.strptime(stored_date, "%Y-%m-%d").date()
        else:
            self.start_date = date.today()

        config.set('Gantt', 'start_date', self.start_date)

        csv_file_name = 'Requerimientos_{}.csv'.format(
            self.context['client_name'])
        csv_file_name = join(output_folder, csv_file_name)

        with open(csv_file_name, 'wb') as csv_file:
            # import csv into md
            self.reformat_csv(input_file, csv_file)
