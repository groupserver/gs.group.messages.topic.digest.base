# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
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
log = getLogger('gs.group.messages.topic.digest.base.vielets')
from gs.group.base import GroupViewlet
from .topicsDigest import BaseTopicsDigest


class HeaderFooterViewlet(GroupViewlet):
    """ Convientently provides basic info for the header and footer"""

    def __init__(self, context, request, view, manager):
        super(HeaderFooterViewlet, self).__init__(context, request, view,
                                                  manager)

        config = getattr(self.context, b'GlobalConfiguration')
        self.emailDomain = config.getProperty(b'emailDomain')
        # --=mpj17=-- vvv Is this right? vvv
        self.groupEmail = '%s@%s' % (self.groupInfo.get_id(),
                                     self.emailDomain)


class TopicsDigestViewlet(GroupViewlet):
    """ Base Topics Digest class. Common code goes here. Not all that useful
        by itself."""

    def __init__(self, context, request, view, manager):
        super(TopicsDigestViewlet, self).__init__(context, request, view,
                                                  manager)
        self.groupTz = self.groupInfo.get_property(b'group_tz', 'UTC')

    @property
    def topicsDigest(self):
        """ Provides the list of topic models in the current digest."""
        assert hasattr(self, '__topicsDigest__')
        retval = self.__topicsDigest__
        assert isinstance(retval, BaseTopicsDigest)
        return retval
