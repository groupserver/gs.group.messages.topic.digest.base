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
from __future__ import absolute_import, unicode_literals, print_function
from mock import (MagicMock, patch)
from unittest import TestCase
from gs.group.messages.topic.digest.base.sendDigests import (
    SendDigest, NoSuchSiteError, NoSuchGroupError)


class SendDigestTest(TestCase):

    def test_get_site_none(self):
        'If the site does not exist'
        context = MagicMock()
        siteRoot = context.site_root()
        siteRoot.Content.ethel = None
        request = MagicMock()
        s = SendDigest(context, request)

        with self.assertRaises(NoSuchSiteError):
            s.get_site('ethel')

    def test_get_site_not_division(self):
        'If the site is not marked as a site'
        context = MagicMock()
        siteRoot = context.site_root()
        siteRoot.Content.ethel.getProperty.return_value = False
        request = MagicMock()
        s = SendDigest(context, request)

        with self.assertRaises(NoSuchSiteError):
            s.get_site('ethel')

    def test_get_site_no_groups(self):
        'If the site is missing the groups folder'
        context = MagicMock()
        siteRoot = context.site_root()
        # Note that the folder 'ethel' does not contain 'groups'
        siteRoot.Content.ethel = MagicMock(spec=['getProperty'])
        siteRoot.Content.ethel.getProperty.return_value = True
        request = MagicMock()
        s = SendDigest(context, request)

        with self.assertRaises(NoSuchSiteError):
            s.get_site('ethel')

    def test_get_site(self):
        'Test actually getting a site'
        context = MagicMock()
        siteRoot = context.site_root()
        ethel = siteRoot.Content.ethel
        ethel.getProperty.return_value = True
        request = MagicMock()
        s = SendDigest(context, request)

        r = s.get_site('ethel')
        self.assertIs(ethel, r)

    @patch.object(SendDigest, 'get_site')
    def test_get_group_none(self, mock_get_site):
        'If the group does not exist'
        ethel = mock_get_site()
        ethel.groups.frog = None
        context = MagicMock()
        request = MagicMock()
        s = SendDigest(context, request)

        with self.assertRaises(NoSuchGroupError):
            s.get_group('ethel', 'frog')

    @patch.object(SendDigest, 'get_site')
    def test_group_not(self, mock_get_site):
        'If the folder exists, but is not a group'
        ethel = mock_get_site()
        ethel.groups.frog.getProperty.return_value = False
        context = MagicMock()
        request = MagicMock()
        s = SendDigest(context, request)

        with self.assertRaises(NoSuchGroupError):
            s.get_group('ethel', 'frog')

    @patch.object(SendDigest, 'get_site')
    def test_group(self, mock_get_site):
        'Actually getting a group'
        ethel = mock_get_site()
        frog = ethel.groups.frog
        frog.getProperty.return_value = True
        context = MagicMock()
        request = MagicMock()
        s = SendDigest(context, request)

        r = s.get_group('ethel', 'frog')
        self.assertIs(frog, r)
