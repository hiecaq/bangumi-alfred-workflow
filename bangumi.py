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

from bangumi import search_for
from workflow import Workflow3


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
        key = 'result-' + hashlib.md5(query.encode('utf-8')).hexdigest()

        items = wf.cached_data(key, lambda: search_for(query), max_age=600)
        for item in items:
            wf.add_item(**item)

        wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3()
    logger = wf.logger
    sys.exit(wf.run(main))
