# -*- coding: utf-8 -*-

""" Requirements generator. """

from csv import DictReader
from os import remove, makedirs
from os.path import exists, join

from pandoc import md_to_pdf_with_template
from datetime import date, datetime, timedelta


class RequirementsGenerator():
    colors = ["grey1", "blue2", "green1", "purple1", "red1", "orange1",
              "blue1", "yellow1"]

    def __init__(self):
        f = open('templates/md/req/requirement_table.md', 'r')
        self.requirement_table_template = f.read()
        f.close()

        f = open('templates/md/req/introduction.md', 'r')
        self.introduction_template = f.read()
        f.close()

        self.initialize()

    def initialize(self):
        self.current_group_name = ""
        self.accumulated_hours = 0
        self.start_date = None
        self.color_index = 0

    def process_requirement(self, requirement, md_file):
        """  Process requirement into Markdown format. """
        requirement_id = int(requirement['ID'])
        if requirement_id % 100 == 0:
            if requirement_id == 1000:
                md_file.write('## 2.2 Requerimientos no funcionales\n')
            md_file.write('### {}\n'.format(requirement['Name/Title']))
        else:
            md_file.write(
                self.requirement_table_template.format(**requirement))

        md_file.write('\n')

    def import_csv(self, input_file, md_file):
        """ Imports the CSV file into Markdown format. """

        with open(input_file, 'rb') as csv_file:
            content = DictReader(csv_file, delimiter=',')
            for requirement in content:
                self.process_requirement(requirement, md_file)

    def reformat_requirement(self, requirement, csv_file):
        """ Creates a new row, using the specified requirement dict """
        requirement_id = int(requirement['ID'])
        if requirement_id % 100 == 0:
            self.current_group_name = requirement['Name/Title']
            self.color_index += 1
            self.color_index %= len(self.colors)
            return

        line = [self.current_group_name, requirement['Name/Title'],
                '"%s"' % requirement['Description']]

        hh = int(requirement['HH'])

        # calculate the start_date
        days = self.accumulated_hours / 8
        start_date = self.start_date + timedelta(days=days)

        week_day = start_date.weekday()
        if week_day == 5 or week_day == 6:
            start_date = self.start_date + timedelta(days=7 - week_day)
        line.append(start_date.isoformat())

        self.accumulated_hours += hh

        days = self.accumulated_hours / 8
        if hh % 8 == 0:
            days = days - 1

        end_date = self.start_date + timedelta(days=days)
        week_day = end_date.weekday()
        if week_day == 5 or week_day == 6:
            end_date = self.end_date + timedelta(days=7 - week_day)

        line.append(end_date.isoformat())

        line.append(self.colors[self.color_index])
        line.append("\n")
        csv_file.write(",".join(line))

    def reformat_csv(self, input_file, csv_file):
        """ Creates a new csv file to be imported to team_gantt """

        with open(input_file, 'rb') as input_csv_file:
            #write the first headers
            csv_file.write(
                'Group,Name/Title,Notes,Start Date,End Date,Color\n')

            content = DictReader(input_csv_file, delimiter=',')
            for requirement in content:
                self.reformat_requirement(requirement, csv_file)

    def create_header(self, md_file):
        """ Creates the header document in Markdown format. """

        context = {
            'project_title': raw_input('Project title: '),
            "client_name": raw_input('Client name: '),
        }

        md_file.write(self.introduction_template.format(**context))

        return context

    def tmp_cleanup(self):
        """ Removes generated tmp files. """

        remove('.tmp.md')

    def generate(self, input_file, output_folder='output'):
        # md output file
        with open('.tmp.md', 'w') as md_file:
            # header creation
            context = self.create_header(md_file)

            # import csv into md
            self.import_csv(input_file, md_file)

        # output to PDF
        if not exists(output_folder):
            makedirs(output_folder)
        md_file = '.tmp.md'
        pdf_file = 'Requerimientos {}.pdf'.format(context['client_name'])
        pdf_file = join(output_folder, pdf_file)
        template = 'templates/requirements.tex'
        md_to_pdf_with_template(md_file, pdf_file, template)

        # tmp files cleanup
        self.tmp_cleanup()
        raw_date = raw_input('Start date (leave blank for today): ')
        if raw_date:
            self.start_date = datetime.strptime(raw_date, "%d%m%Y").date()
        else:
            self.start_date = date.today()

        csv_file_name = 'Requerimientos_{}.csv'.format(context['client_name'])
        csv_file_name = join(output_folder, csv_file_name)
        print csv_file_name
        with open(csv_file_name, 'w') as csv_file:
            # import csv into md
            self.reformat_csv(input_file, csv_file)
