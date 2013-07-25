# -*- coding: utf-8 -*-
""" Tools for the requirements generator classes"""

import errno
import os
import re
import unicodedata


def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = unicode(value)
    value = value.lower()
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = value.decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def project_path(context):
    client_name = slugify(context['client_name'])
    project_name = slugify(context['project_name'])

    project_path = "clients/%s/%s" % (client_name, project_name)

    try:
        os.makedirs(project_path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(project_path):
            pass
        else:
            raise

    return project_path
