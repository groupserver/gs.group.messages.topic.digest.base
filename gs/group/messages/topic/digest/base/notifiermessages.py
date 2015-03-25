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
from gs.group.base import GroupPage


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
