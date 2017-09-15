# -*- coding: utf-8 -*-
"""
    bangumi-alfred-workflow.bangumi.search
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The search utility for bgm.tv

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

from workflow import web

ICON = 'icon.png'

TYPE = {1: '书籍', 2: '动画', 3: '音乐', 4: '游戏', 6: '三次元'}

URL = 'https://api.bgm.tv/search/subject/{0}'


def _get_raw_result(query):
    """Return the search result of this query as a list

    :param str query: the text wish to test
    :returns: a list of pre-edited items

    """
    url = URL.format(query)
    params = {'responseGroup': 'simple', 'max_results': '11', 'start': '0'}
    r = web.get(url, params)
    r.raise_for_status()

    result = r.json()
    return result['list']


def search_for(query):
    """Return the search result of this query as a list of post-processed
    items

    :param str query: the text wish to search
    :returns: a list of post-processed items

    """
    raw = _get_raw_result(query)

    items = [
        dict(
            title=item['name'],
            subtitle=(
                TYPE[item['type']] + ' - ' + item['name_cn']
                if item['name_cn'] else TYPE[item['type']]
            ),
            arg=item['url'],
            valid=True,
            icon=ICON
        ) for item in raw
    ]

    return items
