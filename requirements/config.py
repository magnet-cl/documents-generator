# -*- coding: utf-8 -*-
""" A config parser for a requirement generator proyect """

import ConfigParser
from requirements import utils
from os.path import exists


class RequirementsConfigParser(object):
    """ A parser for the config file of a requirements project """

    def __init__(self, context):
        self.config_path = "%s/config.cfg" % utils.project_path(context)
        self.config = ConfigParser.ConfigParser()

        self.sections = ('Gantt', 'Requirements')
        for section in self.sections:
            try:
                self.config.add_section(section)
            except ConfigParser.DuplicateSectionError:
                pass

        self.readfp()

    def readfp(self):
        if exists(self.config_path):
            self.config.readfp(open(self.config_path))

    def write(self):
        with open(self.config_path, 'wb') as configfile:
            self.config.write(configfile)

    def get(self, *args, **kwargs):
        try:
            return self.config.get(*args, **kwargs)
        except ConfigParser.NoOptionError:
            return None

    def set(self, *args, **kwargs):
        self.config.set(*args, **kwargs)
        self.write()
