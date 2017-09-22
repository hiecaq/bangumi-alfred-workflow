# -*- coding: utf-8 -*-
"""
    bangumi-alfred-workflow.bangumi.login
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The login utility for bgm.tv

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

from workflow import ICON_ERROR


def login(text):
    """Login with the given text; return an item saying error if failed

    :param str text: the text contain email address and password for loginning
    :returns: a list of items

    """
    info = text.strip().split()
    if len(info) != 2:
        return [
            dict(
                title='Wrong input',
                subtitle='Please use the format <email> <password>',
                valid=False,
                icon=ICON_ERROR
            )
        ]
