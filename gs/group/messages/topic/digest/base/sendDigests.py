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
from __future__ import absolute_import, unicode_literals
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.base import SiteForm
from gs.auth.token import log_auth_error
from .interfaces import ISendAllDigests, ITopicsDigestNotifier
from .notifiers import NoSuchListError

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.sendDigests')
FOLDER_TYPES = ['Folder', 'Folder (Ordered)']


class SendAllDigests(SiteForm):
    label = 'Send Digests for All Groups on the Site'
    pageTemplateFileName = 'browser/templates/send_all_digests.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(ISendAllDigests, render_context=False)

    def setUpWidgets(self, ignore_request=False):
        data = {'name': self.siteInfo.name, }
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)

    @property
    def sites(self):
        '''All sites in a GroupServer instance'''
        # The digest sender sends digests for all groups the share the same
        # GroupServer *INSTANCE* as the site we currently on. This iterator
        # gets all the sites.
        # TODO: Put in a generic place (gs.site.base?)
        site_root = self.context.site_root()
        content = getattr(site_root, 'Content')
        sIds = content.objectIds(FOLDER_TYPES)
        for sId in sIds:
            s = getattr(content, sId)
            if s.getProperty('is_division', False) and hasattr(s, 'groups'):
                yield s

    def groups_for_site(self, site):
        '''An iterator for all groups on a site.'''
        # --=mpj17=-- I am using an iterator so we do not load all the group
        # instances into RAM in one hit. ('groupserver.GroupsInfo' needs to
        # be fixed so it treads lightly on RAM.)
        groups = getattr(site, 'groups')
        gIds = groups.objectIds(FOLDER_TYPES)
        for gId in gIds:
            g = getattr(groups, gId)
            if (g.getProperty('is_group', False)):
                yield g

    @form.action(label='Send', failure='handle_send_all_digests_failure')
    def handle_send_all_digests(self, action, data):
        log.info('Processing the digests')
        # FIXME: iterate through just the groups that need to have a digest
        # We do not need to iterate through all of the sites and all the
        # groups: a query on the email-settings table will get us the groups
        # we need to concern ourselves with.
        for site in self.sites:
            for group in self.groups_for_site(site):
                try:
                    tdn = getMultiAdapter((group, self.request),
                                          ITopicsDigestNotifier)
                except ComponentLookupError:
                    m = 'Ignoring the group with the odd interface: {0} '\
                        'on {1}'
                    log.warn(m.format(site.getId(), group.getId()))

                try:
                    tdn.notify()
                except NoSuchListError as nsle:
                    # The Group esits but there is no coresponding mailing
                    # list
                    log.warn(nsle)

        log.info('All digests sent')
        self.status = '<p>All digests sent.</p>'

    def handle_send_all_digests_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) == 1:
            self.status = '<p>There is an error:</p>'
