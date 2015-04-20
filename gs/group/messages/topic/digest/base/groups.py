# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from json import dumps as to_json
from logging import getLogger
log = getLogger('gs.group.messages.topic.digest.base.groups')
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from gs.content.form.api.json import SiteEndpoint
from gs.auth.token import log_auth_error
from .interfaces import (IGetDigestGroups)
from .queries import DigestGroupsQuery


class GetGroups(SiteEndpoint):
    '''The page that gets a list of groups to send the digest to'''
    label = 'Get the digest groups'
    form_fields = form.Fields(IGetDigestGroups, render_context=False)

    @form.action(label='Get', name='get', prefix='',
                 failure='handle_get_all_digests_failure')
    def handle_get_all_digests(self, action, data):
        '''The form action for the *Get digest groups* page.

:param action: The button that was clicked.
:param dict data: The form data.'''
        log.info('Getting the digest groups')
        retval = self.get_groups()
        return to_json(retval)

    def handle_get_all_digests_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        retval = self.build_error_response(action, data, errors)
        return retval

    # --=mpj17=-- Everything below here could be in a seperate Groups class
    # FWIW

    def get_groups(self):
        groups = set()
        for siteId, groupId in self.queries.get_digest_groups():
            if not(siteId):
                siteId = self.get_siteId_for_group(groupId)
            if siteId:
                # If we cannot figure out the site then no need to process
                # the digest
                r = (siteId, groupId)
                groups.add(r)
        retval = list(groups)  # sets are not serialisable
        return retval

    @Lazy
    def queries(self):
        retval = DigestGroupsQuery()
        return retval

    def get_siteId_for_group(self, groupId):
        mailingList = getattr(self.listManager, groupId, None)
        retval = ''
        if mailingList is not None:
            retval = mailingList.getProperty('siteId')
        return retval

    @Lazy
    def listManager(self):
        retval = getattr(self.context, 'ListManager', None)
        if retval is None:
            raise ValueError('Failed to acquire the ListManager')
        return retval
