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
from zope.viewlet.interfaces import IViewletManager
from zope.interface import Interface
from gs.auth.token import AuthToken


class IDailyTopicsDigestHtmlVM(IViewletManager):
    ''' Viewlet manager for daily topics digests '''


class IDailyTopicsDigestTxtVM(IViewletManager):
    ''' Viewlet manager for daily topics digests '''


class IWeeklyTopicsDigestHtmlVM(IViewletManager):
    ''' Viewlet manager for weekly topics digests '''


class IWeeklyTopicsDigestTxtVM(IViewletManager):
    ''' Viewlet manager for weekly topics digests '''


class ISendAllDigests(Interface):
    '''Declares the form that will be used to send digests for all of the
    groups on the site. '''

    token = AuthToken(
        title='Token',
        description='The authentication token',
        required=True)


class ITopicsDigestNotifier(Interface):

    def notify():
        'Send out the topic digest to the group'
