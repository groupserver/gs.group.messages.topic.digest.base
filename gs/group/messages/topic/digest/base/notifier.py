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
log = getLogger('gs.group.messages.topic.digest.base.notifier')
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.email import send_email
from .message import Message
from .queries import SendQuery
UTF8 = 'utf-8'


class NoSuchListError(AttributeError):
    'No such list exists.'
    pass


class DigestNotifier(object):
    '''Send a new digest notification to all the group members that want
to recieve a digest

:param object group: The group to send the digest to.
:param object request: The HTTP request object.'''
    def __init__(self, group, request):
        self.context = self.group = group
        self.request = request

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.group)
        return retval

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.group)
        if not retval:
            msg = 'Could not create the GroupInfo from %s' % self.group
            raise ValueError(msg)
        return retval

    @Lazy
    def acl_users(self):
        site_root = self.context.site_root()
        retval = site_root.acl_users
        return retval

    def check_address(self, a):
        '''Check if the address is valid

:param str a: The address to check.
:returns: ``True`` if the address is valid; ``False`` otherwise.
:rtype: bool

An address is considered valid if it contains an ``@`` and the address is
associated with profile of a user.'''
        retval = ('@' in a) and self.acl_users.get_userIdByEmail(a.lower())
        return retval

    @Lazy
    def digestMemberAddresses(self):
        '''The list of email addresses of the group members that are
configured to receive a digest.'''
        try:
            mListInfo = createObject('groupserver.MailingListInfo',
                                     self.group)
        except AttributeError:
            # Turn the generic AttributeError to the more specific
            # NoSuchListError.
            # TODO: Move the error class and this code to the mailing list
            m = 'No such list "{0}" on {1}'
            msg = m.format(self.groupInfo.id, self.siteInfo.id)
            raise NoSuchListError(msg)
        mlist = mListInfo .mlist
        rawList = mlist.getValueFor('digestmaillist') or []
        # Only return real addresses for real users
        cleanAddresses = [a for a in rawList if self.check_address(a)]
        # Sort by mail-host.
        retval = sorted(cleanAddresses, key=lambda s: s[::-1])
        assert type(retval) == list
        return retval

    @Lazy
    def sendQuery(self):
        retval = SendQuery()
        return retval

    @Lazy
    def digest_sent_today(self):
        '``True`` if we have sent a digest today; ``False`` otherwise.'
        retval = self.sendQuery.has_digest_since(self.siteInfo.id,
                                                 self.groupInfo.id)
        return retval

    def notify(self, subject, text, html):
        """Notifiy the members of the group that are on the digest

:param str subject: The subject of the digest email
:param str text: The ``text/plain`` version of the digest message
:param str html: The ``text/html`` version of the digest message
:returns: None
:raises gs.group.messages.topic.digest.base.notifier.NoSuchListError: if no
    mailing-list could be found to match the group.

Creates a message based on the parameters (:class:`.message.Message`) and
then sends the digest email to members of the group who are subscribed to
topics digests, if the information from the database indicates that a
digest has not be sent today.

A digest log is also checked and modified. If the log shows that a digest
has been sent to the group in the previous 24 hours, a digest will not be
created and sent. If a digest is created and sent, the log will be updated
to reflect when the digest emails were sent."""
        if ((len(self.digestMemberAddresses) > 0)
                and (not self.digest_sent_today)):
            message = Message(self.group, subject, text, html)
            messageString = str(message)
            send_email(message.rawFromAddress, self.digestMemberAddresses,
                       messageString)
            self.sendQuery.update_group_digest(self.siteInfo.id,
                                               self.groupInfo.id)

            m = 'Sent digest of length {0} from {1} on {2} to {3} address.'
            msg = m.format(len(messageString), self.groupInfo.id,
                           self.siteInfo.id,
                           len(self.digestMemberAddresses))
            log.info(msg)
