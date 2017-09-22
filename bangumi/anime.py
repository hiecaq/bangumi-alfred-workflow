# -*- coding: utf-8 -*-
"""
    bangumi-alfred-workflow.bangumi.anime
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Code that deals with anime in bgm.tv

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

from workflow import web

ICON = 'icon.png'


class Animelist(object):
    """Manipulate the bgm api about anime"""

    def __init__(self, uid, auth):
        """Return an Animelist object with the given uid and auth token.

        :param str uid: the uid of this user
        :param str auth: the auth token of this user

        """
        self._uid = uid
        self._auth = auth

    def watchlist(self):
        """Return a list of items containing watching anime

        :returns: list of items

        """
        url = (
            'https://api.bgm.tv/user/' + self._uid + '/collection?cat=watching'
        )
        r = web.get(url)
        r.raise_for_status()
        raw = r.json()

        items = [
            dict(
                title=item['subject']['name'],
                subtitle=(
                    str(item['ep_status']) + '/' + str(item['subject']['eps'])
                    + ' - ' + item['subject']['name_cn']
                ),
                arg=item['subject']['id'],
                valid=True,
                icon=ICON
            ) for item in raw
        ]
        return items
