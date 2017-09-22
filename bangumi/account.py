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


def login(text, wf):
    """Login with the given text; return an item saying error if failed

    :param str text: the text contain email address and password for loginning
    :param workflow.Workflow3 wf: the Workflow3 object this script works on
    :returns: a list of items

    """

    if 'UID' in wf.settings and text != 'logout':
        return [
            dict(
                title='Already logging into ' + wf.settings['UID'],
                subtitle=(
                    'If you want to switch to another account, '
                    'please log out first.'
                ),
                valid=False,
                icon=ICON_WARNING
            )
        ]

    if text == 'logout':
        try:
            del wf.settings['UID']
            wf.delete_password('bangumi-auth-token')
        except Exception as e:
            return [
                dict(
                    title='You are not logged into any account.',
                    subtitle='Please Logging into anything first.',
                    valid=False,
                    icon=ICON_ERROR
                )
            ]
        else:
            return [
                dict(
                    title='Logout sucessfully.',
                    subtitle=(
                        'You successfully logout from the previous account.'
                    ),
                    valid=False,
                    icon=ICON_INFO
                )
            ]

    info = text.split()
    if len(info) != 2:
        return [
            dict(
                title='Wrong input',
                subtitle='Please use the format <email> <password>',
                valid=False,
                icon=ICON_ERROR
            )
        ]

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

        return [
            dict(
                title='Log in success.',
                subtitle='Sucessfully logging into ' + output['username'],
                valid=False,
                icon=ICON_INFO
            )
        ]
    else:
        return [
            dict(
                title='Log in failed.',
                subtitle=(
                    'ERROR ' + str(output['code']) + ': ' + output['error']
                ),
                valid=False,
                icon=ICON_ERROR
            )
        ]
