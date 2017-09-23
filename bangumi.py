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

from bangumi import Animelist, login, search_for
from workflow import Workflow3


def save_name(prefix, name):
    """Return the hashed save name for the given name

    :param str prefix: the prefix for this name
    :param str name: the name need to be
    :returns: a string as the save name

    """
    return prefix + '-' + hashlib.md5(name.encode('utf-8')).hexdigest()


def filter_key(item):
    """Generate a filter key for the item.

    """
    return item['title'] + ' ' + item['subtitle']


def cache_filter(item):
    """help method to filter cache that should be cleaned

    """
    return item.startswith('watchlist')


class LogoutException(Exception):
    """Exception raised when the user haven't login"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def get_anime_list(wf):
    """Get an Animelist instance.

    :param Workflow3 wf: the Workflow3 object
    :returns: Animelist object
    :rtype: Animelist
    """
    try:
        animelist = Animelist(
            wf.settings['UID'], wf.get_password('bangumi-auth-token')
        )
    except Exception as e:
        raise LogoutException("Please login first")
    else:
        return animelist


def main(wf):
    """Setup the workflow with items

    :param Workflow3 wf: the Workflow3 object this script works on

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', dest='query', nargs='?', default=None)
    parser.add_argument('--setkey', dest='input', nargs='?', default=None)
    parser.add_argument(
        '--watching', dest='watchlist', nargs='?', default=None
    )
    parser.add_argument('--update', dest='episode', nargs='?', default=None)
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

    ##############
    #  watching  #
    ##############
    if args.watchlist is not None:
        query = args.watchlist
        animelist = get_anime_list(wf)
        items = wf.cached_data('watchlist', animelist.watchlist, max_age=600)
        if query:
            items = wf.filter(query, items, key=filter_key)

    if args.episode:
        animelist = get_anime_list(wf)
        watched = animelist.update(args.episode)
        if watched:
            wf.clear_cache(cache_filter)
        return 0

    for item in items:
        wf.add_item(**item)

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3()
    logger = wf.logger
    sys.exit(wf.run(main))
