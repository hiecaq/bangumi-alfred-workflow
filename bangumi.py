#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

from workflow import Workflow3, web

ICON = 'icon.png'

TYPE = {1: '书籍', 2: '动画', 3: '音乐', 4: '游戏', 6: '三次元'}


def get_search_result(query):
    """TODO: Docstring for get_search_result.

    :query: TODO
    :returns: TODO

    """
    url = 'https://api.bgm.tv/search/subject/{0}'.format(query)
    params = {'responseGroup': 'simple', 'max_results': '11', 'start': '0'}
    r = web.get(url, params)
    r.raise_for_status()

    result = r.json()
    return result['list']


def main(wf):
    query = wf.args[0]

    items = wf.cached_data(
        'result:' + query, lambda: get_search_result(query), max_age=600
    )

    for item in items:
        wf.add_item(
            title=item['name_cn'],
            subtitle=TYPE[item['type']] + ' - ' + item['name'],
            arg=item['url'],
            valid=True,
            icon=ICON
        )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3()
    logger = wf.logger
    sys.exit(wf.run(main))
