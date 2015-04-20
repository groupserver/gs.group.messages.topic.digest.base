# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2013, 2014, 2015 E-Democracy.org and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import unicode_literals
from zope.interface import Interface
from zope.schema import ASCIILine, Bool, Int, Text, TextLine
from gs.auth.token import AuthToken


class IGetDigestGroups(Interface):
    'Get the digest groups'
    token = AuthToken(
        title='Token',
        description='The authentication token',
        required=True)


class ISendDigest(Interface):
    '''Declares the form that will be used to send digest to a group on the
site.'''

    siteId = ASCIILine(
        title='Site Identifier',
        required=True)

    groupId = ASCIILine(
        title='Group Identifier',
        required=True)

    token = AuthToken(
        title='Token',
        description='The authentication token',
        required=True)


class ITopicsDigestNotifier(Interface):

    canSend = Bool(
        title='Can send the digest',
        description='True if the notifier can send the digest.',
        required=True)

    weight = Int(
        title='Weight',
        description='When multiple notifiers can send the digest the '
                    'weight determines the one that is sent.',
        required=True)

    subject = TextLine(
        title='Subject',
        description='The subject of the email that will contain the digest',
        required=True)

    text = Text(
        title='Text',
        description='The text/plain version of the digest.',
        required=True)

    html = Text(
        title='HTML',
        description='The text/html version of the digest.',
        required=True)

    def notify():
        'Send out the topic digest to the group'
