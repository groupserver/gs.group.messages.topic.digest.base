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
from logging import getLogger
log = getLogger('gs.group.messages.topic.digest.base.send')
from zope.component import getAdapters
from zope.component.interfaces import ComponentLookupError
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.base import SiteForm
from gs.auth.token import log_auth_error
from .interfaces import (ISendDigest, ITopicsDigestNotifier)
from .notifier import (DigestNotifier, NoSuchListError)
FOLDER_TYPES = ['Folder', 'Folder (Ordered)']


class NoSuchObjectError(ValueError):
    '''Base class for the :class:`NoSuchSiteError` and
:class:`NoSuchGroupError`

:param str val: The identifier for the object that could not be found.
:param str msg: The error message.'''

    def __init__(self, val, msg):
        super(NoSuchObjectError, self).__init__(msg)
        self.value = val


class NoSuchSiteError(NoSuchObjectError):
    'The specified site does not exsit'


class NoSuchGroupError(NoSuchObjectError):
    'The specified group does not exist'


class SendDigest(SiteForm):
    '''The page that sends a digest to a group'''

    label = 'Send a digest to a group'
    pageTemplateFileName = 'browser/templates/send_all_digests.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(ISendDigest, render_context=False)

    def get_site(self, siteId):
        '''Get a site

:param str siteId: The site identifier
:returns: The site object for the ID.
:raises gs.group.messages.topic.digest.base.sendDigests.NoSuchSiteError: The
    specified site does not exist'''
        site_root = self.context.site_root()
        content = getattr(site_root, 'Content')
        retval = getattr(content, siteId, None)
        if ((retval is None) or not retval.getProperty('is_division', False)
                or not hasattr(retval, 'groups')):
            m = 'No site with the ID "{0}"'.format(siteId)
            raise NoSuchSiteError(siteId, m)
        return retval

    def get_group(self, siteId, groupId):
        '''Get a group

:param str siteId: The site identifier
:param str groupId: The group identifier
:returns: The group object on the site.
:raises gs.group.messages.topic.digest.base.sendDigests.NoSuchGroupError:
    The group does not exist.

The :meth:`.sendDigests.SendDigest.get_site` method is called to get the
site, which is then examined to get the group.'''
        site = self.get_site(siteId)
        groups = getattr(site, 'groups')
        retval = getattr(groups, groupId, None)
        if ((retval is None) or not retval.getProperty('is_group', False)):
            m = 'No group with the ID "{0}" on the site "{1}"'
            msg = m.format(groupId, siteId)
            raise NoSuchGroupError(groupId, msg)
        return retval

    def get_digest_adapter(self, group):
        '''Get the digest adaptor for a group

:param object group: The group to get a digest-adaptor for.
:returns: The "best" digest adaptor for the group, or ``None``.
:rtype: :class:`.interfaces.ITopicsDigestNotifier`'''
        adapters = [a[1] for a in getAdapters((group, self.request),
                                              ITopicsDigestNotifier)
                    if a[1].canSend]
        adapters.sort(key=lambda a: a.weight)
        retval = adapters[0] if adapters else None
        return retval

    @form.action(label='Send', name='send',
                 failure='handle_send_all_digests_failure')
    def handle_send_all_digests(self, action, data):
        '''The form action for the *Send digest* page.

:param action: The button that was clicked.
:param dict data: The form data, containing the keys ``siteId`` and
    ``groupId``.

The group (:meth:`.sendDigests.SendDigest.get_group`) is adapted to a digest
(:meth:`.sendDigests.SendDigest.get_digest_adpter`). This digest is then
sent to the group members using the notifier
(:class:`.notifier.DigestNotifier`).'''
        m = 'Processing the digests for "{0}" on "{1}"'
        msg = m.format(data['siteId'], data['groupId'])
        log.info(msg)

        try:
            group = self.get_group(data['siteId'], data['groupId'])
        except NoSuchSiteError as nsse:
            log.warn(nsse)
            self.satus = '<p>No digest sent</p>'
            return  # Sorry, Dijkstra
        except NoSuchGroupError as nsge:
            log.warn(nsge)
            self.satus = '<p>No digest sent</p>'
            return  # Sorry, Dijkstra

        try:
            tdn = self.get_digest_adapter(group)
        except ComponentLookupError:
            m = 'Ignoring the group with the odd interface: """'
            log.warn(m.format(data['siteId'], data['groupId']))

        if tdn:  # There may not be any digest for today
            try:
                notifier = DigestNotifier(group, self.request)
                notifier.notify(tdn.subject, tdn.text, tdn.html)
            except NoSuchListError as nsle:
                # The Group exits but there is no coresponding mailing list
                log.warn(nsle)
            else:
                m = 'Digests sent to "{0}" on "{1}"'
                msg = m.format(data['siteId'], data['groupId'])
                log.info(msg)
        else:
            m = 'No digests to send to "{0}" on "{1}"'
            msg = m.format(data['siteId'], data['groupId'])
            log.info(msg)
        self.request.response.setHeader(b'Content-type', b'text/html')
        self.status = '<p>All digests sent.</p>'

    def handle_send_all_digests_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) == 1:
            self.status = '<p>There is an error:</p>'
