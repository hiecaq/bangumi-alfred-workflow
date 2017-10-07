# -*- coding: utf-8 -*-
"""
    bangumi-alfred-workflow.bangumi.anime
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Code that deals with anime in bgm.tv

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

from time import sleep

from workflow import web
from workflow.notify import notify

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
                autocomplete=item['subject']['name'],
                icon=ICON
            ) for item in raw
        ]
        return items

    def anime_episodes(self, subject):
        """Get the info about one anime.
        Note that due to the limitation of the api,
        two requests must be done here.

        :param str subject: the id of this anime
        :returns: dict

        """
        url = (
            'https://api.bgm.tv/subject/'
            '{0}?responseGroup=large'.format(subject)
        )
        r = web.get(url)
        r.raise_for_status()
        eps = r.json()['eps']
        return [str(ep['id']) for ep in eps]

    def watch_status(self, subject):
        """Get the watch status about one anime.

        :param str subject: the id of this anime
        :returns: how many episodes have been watched
        :rtype: int

        """
        url = 'https://api.bgm.tv/user/{0}/progress'.format(self._uid)
        params = {'source': 'onAir', 'auth': self._auth, 'subject_id': subject}
        r = web.get(url, params=params)
        r.raise_for_status()
        return len(r.json()['eps']) if r.content != 'null' else 0

    def update(self, subject):
        """Mark the next episode as watched.

        :param str subject: the id of this anime
        :returns: TODO

        """
        watched = self.watch_status(subject)
        sleep(1)
        eps = self.anime_episodes(subject)
        if watched < len(eps):
            url = (
                'https://api.bgm.tv/ep/'
                '{0}/status/watched?source=onAir'.format(eps[watched])
            )
            data = {'auth': self._auth}
            r = web.post(url, data=data)
            r.raise_for_status()

            result = r.json()
            if result['code'] == 200:
                episode = str(watched + 1)
                notify(
                    "Bangumi", (
                        "Sucessfully mark episode {0} as watched!".
                        format(episode)
                    )
                )
                return episode
            else:
                notify(
                    "Bangumi",
                    "Error {0}: {1}".format(result['code'], result['error'])
                )

        return -1
