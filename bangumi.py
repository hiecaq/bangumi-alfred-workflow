#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    bangumi-alfred-workflow.bangumi
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    An Alfred Workflow for bgm.tv

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import argparse
import hashlib
import sys

from bangumi import login, search_for
from workflow import Workflow3


def save_name(prefix, name):
    """Return the hashed save name for the given name

    :param str prefix: the prefix for this name
    :param str name: the name need to be
    :returns: a string as the save name

    """
    return prefix + '-' + hashlib.md5(name.encode('utf-8')).hexdigest()


def main(wf):
    """Setup the workflow with items

    :param Workflow3 wf: the Workflow3 object this script works on

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', dest='query', nargs='?', default=None)
    parser.add_argument('--setkey', dest='input', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    ############
    #  search  #
    ############
    if args.query:
        query = args.query
        items = wf.cached_data(
            save_name('result', query), lambda: search_for(query), max_age=600
        )

    #############
    #  set key  #
    #############
    if args.input:
        query = args.input
        items = wf.cached_data(
            save_name('login', query), lambda: login(query, wf), max_age=60
        )

    for item in items:
        wf.add_item(**item)

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3()
    logger = wf.logger
    sys.exit(wf.run(main))
