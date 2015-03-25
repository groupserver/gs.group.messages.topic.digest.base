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
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.utils import formataddr
from zope.i18nmessageid import MessageFactory
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
_ = MessageFactory('groupserver')
utf8 = 'utf-8'


class Message(object):
    # TODO: Create and use a MessageSender made for notifying groups
    def __init__(self, group):
        self.context = self.group = group

    @Lazy
    def siteInfo(self):
        assert self.context
        retval = createObject('groupserver.SiteInfo', self.context)
        assert retval, 'Could not create the site info'
        return retval

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        assert retval, 'Could not create the GroupInfo from %s' % self.context
        return retval

    @Lazy
    def mailingListInfo(self):
        retval = createObject('groupserver.MailingListInfo', self.context)
        assert retval, 'Cound not create the MailingListInfo instance from '\
            '%s' % self.context
        return retval

    @Lazy
    def toAddress(self):
        address = self.mailingListInfo.get_property('mailto')
        retval = formataddr((self.groupInfo.name, address))
        return retval

    @Lazy
    def rawFromAddress(self):
        retval = self.mailingListInfo.get_property('mailto')
        return retval

    @Lazy
    def fromAddress(self):
        retval = formataddr((self.groupInfo.name, self.rawFromAddress))
        return retval

    def h(self, h):
        'Turn the text h into a nice header string'
        retval = str(Header(h, utf8))
        assert retval
        return retval

    def add_headers(self, container, subject):
        # Required headers
        container['Subject'] = self.h(subject)
        container['From'] = self.fromAddress
        container['To'] = self.toAddress
        # Nice-to-have headers
        container['Precedence'] = 'Bulk'
        container['Organization'] = self.h(self.siteInfo.name)
        # User-Agent is not actually a real header, but Mozilla and MS use it.
        brag = 'GroupServer (gs.groups.messages.topicsdigest)'
        container['User-Agent'] = self.h(brag)

        # RFC2369 headers: <http://tools.ietf.org/html/rfc2369>
        try:
            p = '<mailto:{0}>'.format(self.rawFromAddress)
            container['List-Post'] = self.h(p)

            u = '<mailto:{0}?Subject=Unsubscribe>'.format(self.rawFromAddress)
            container['List-Unsubscribe'] = self.h(u)

            a = '<{0}> (Archive of {1})'\
                .format(self.groupInfo.url, self.groupInfo.name.encode(utf8))
            container['List-Archive'] = self.h(a)

            helpS = '<{0}/help> (Help)'.format(self.siteInfo.url)
            container['List-Help'] = self.h(helpS)

            s = '<mailto:{0}> ({1} Support)'.format(
                self.siteInfo.get_support_email(),
                self.siteInfo.name.encode(utf8))
            container['List-Owner'] = self.h(s)
        except UnicodeDecodeError:
            # FIXME: Sometimes data is just too messed up.
            # http://farmdev.com/talks/unicode/
            pass

        return container

    def create_message(self, subject, txtMessage, htmlMessage):
        # Stolen from gs.profile.notify.sender.MessageSender
        container = MIMEMultipart('alternative')
        container = self.add_headers(container, subject)

        # Construct the body
        txt = MIMEText(txtMessage.encode(utf8), 'plain', utf8)
        container.attach(txt)
        html = MIMEText(htmlMessage.encode(utf8), 'html', utf8)
        container.attach(html)

        retval = container.as_string()
        assert retval
        return retval
