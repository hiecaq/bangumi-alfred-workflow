#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    bangumi-alfred-workflow
    ~~~~~~~~~~~~~~~~~~~~~~~

    An Alfred Workflow for bgm.tv

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import sys

from workflow import Workflow3, web

ICON = 'icon.png'

TYPE = {1: '书籍', 2: '动画', 3: '音乐', 4: '游戏', 6: '三次元'}


def get_search_result(query):
    """Return the search result of this query as a list

    :param str query: the text wish to test
    :returns: a list of pre-edited items

    """
    url = 'https://api.bgm.tv/search/subject/{0}'.format(query)
    params = {'responseGroup': 'simple', 'max_results': '11', 'start': '0'}
    r = web.get(url, params)
    r.raise_for_status()

    result = r.json()
    return result['list']


def main(wf):
    """Setup the workflow with items

    :param Workflow3 wf: the Workflow3 object this script works on

    """
    query = wf.args[0]

    items = wf.cached_data(
        'result:' + query, lambda: get_search_result(query), max_age=600
    )

    for item in items:
        wf.add_item(
            title=item['name'],
            subtitle=(
                TYPE[item['type']] + ' - ' + item['name_cn']
                if item['name_cn'] else TYPE[item['type']]
            ),
            arg=item['url'],
            valid=True,
            icon=ICON
        )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3()
    logger = wf.logger
    sys.exit(wf.run(main))
