# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.notifiermessages')
from zope.cachedescriptors.property import Lazy
from gs.core import to_ascii
from gs.group.base import GroupPage
from .topicsDigest import DailyTopicsDigest, WeeklyTopicsDigest


class TopicsDigestMessage(GroupPage):
    def __init__(self, context, request):
        super(TopicsDigestMessage, self).__init__(context, request)

    @property
    def digest(self):
        raise NotImplementedError

    def __call__(self, topicsDigest=None):
        digest = self.digest if topicsDigest is None else topicsDigest
        s = super(TopicsDigestMessage, self)
        retval = s.__call__(topicsDigest=digest)
        return retval


class WeeklyMessage(TopicsDigestMessage):
    @Lazy
    def digest(self):
        retval = WeeklyTopicsDigest(self.context, self.siteInfo)
        return retval


class WeeklyMessageText(WeeklyMessage):
    def __call__(self, topicsDigest=None):
        retval = super(WeeklyMessageText, self).__call__(topicsDigest)
        c = to_ascii("text/plain; charset=UTF-8")
        self.request.response.setHeader(to_ascii("Content-Type"), c)
        return retval


class DailyMessage(TopicsDigestMessage):
    @Lazy
    def digest(self):
        retval = DailyTopicsDigest(self.context, self.siteInfo)
        return retval


class DailyMessageText(DailyMessage):
    def __call__(self, topicsDigest=None):
        retval = super(DailyMessageText, self).__call__(topicsDigest)
        c = to_ascii("text/plain; charset=UTF-8")
        self.request.response.setHeader(to_ascii("Content-Type"), c)
        return retval
