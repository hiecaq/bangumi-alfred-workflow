# -*- coding: utf-8 -*-
"""
    bangumi-alfred-workflow.bangumi.login
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The login utility for bgm.tv

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

from workflow import ICON_ERROR, ICON_INFO, ICON_WARNING, web

URL = 'https://api.bgm.tv/auth?source=onAir'


def _event(title, subtitle, icon):
    """Build a event used as returned item

    :param str title: the title of this item
    :param str subtitle: the subtitle of this item
    :icon: the icon for this item
    :returns: a list of dict, actually just one entry

    """
    return [dict(title=title, subtitle=subtitle, valid=False, icon=icon)]


def login(text, wf):
    """Login with the given text; return an item saying error if failed

    :param str text: the text contain email address and password for loginning
    :param workflow.Workflow3 wf: the Workflow3 object this script works on
    :returns: a list of items

    """

    if 'UID' in wf.settings and text != 'logout':
        return _event(
            'Already logging into ' + wf.settings['UID'],
            'If you want to switch to another account, please log out first.',
            ICON_WARNING
        )

    if text == 'logout':
        try:
            del wf.settings['UID']
            wf.delete_password('bangumi-auth-token')
        except Exception as e:
            return _event(
                'You are not logged into any account.',
                'Please Logging into anything first.', ICON_ERROR
            )
        else:
            return _event(
                'Logout sucessfully.',
                'You successfully logout from the previous account.', ICON_INFO
            )

    info = text.split()
    if len(info) != 2:
        return _event(
            'Wrong input', 'Please use the format <email> <password>',
            ICON_ERROR
        )

    email, password = info
    data = {
        'password': password,
        'username': email,
        'auth': 0,
        'sysuid': 0,
        'sysusername': 0
    }
    r = web.post(URL, data=data)
    r.raise_for_status()
    output = r.json()

    if 'username' in output:
        wf.settings['UID'] = output['username']
        wf.save_password('bangumi-auth-token', output['auth'])

        return _event(
            'Log in success.',
            'Sucessfully logging into ' + output['username'], ICON_INFO
        )
    else:
        return _event(
            'Log in failed.',
            'ERROR ' + str(output['code']) + ': ' + output['error'], ICON_ERROR
        )
