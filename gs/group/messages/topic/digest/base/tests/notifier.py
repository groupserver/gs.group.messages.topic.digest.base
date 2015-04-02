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
#from mock import (MagicMock, patch)
from unittest import TestCase
from gs.group.messages.topic.digest.base.notifier import (DigestNotifier)


class DigestNotifierTest(TestCase):

    def test_check_address_junk(self):
        'Garbage in, garbage stopped'
        n = DigestNotifier(None, None)
        r = n.check_address('This is not an address')
        self.assertFalse(r)
