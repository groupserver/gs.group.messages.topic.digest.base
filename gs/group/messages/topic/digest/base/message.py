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
try:
    from urllib import parse as urlparse  # Python 3
except ImportError:
    from urlparse import urlparse  # Python 2
    from zope.i18nmessageid import MessageFactory
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
_ = MessageFactory('groupserver')
utf8 = 'utf-8'


class Message(object):
    '''Create an email message for sending to the digest members

:param object group: The group that the digest is for.
:param str subject: The subject of the message.
:param str text: The plain-text version of the digest.
:param str html: THe HTML version of the digest.'''

    # TODO: Create and use a MessageSender made for notifying groups
    def __init__(self, group, subject, text, html):
        self.context = self.group = group
        self.subject = subject
        self.text = text
        self.html = html

    @Lazy
    def siteInfo(self):
        assert self.context
        retval = createObject('groupserver.SiteInfo', self.context)
        assert retval, 'Could not create the site info'
        return retval

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        assert retval, 'Could not create the GroupInfo from '\
                       '"%s"' % self.context
        return retval

    @Lazy
    def mailingListInfo(self):
        retval = createObject('groupserver.MailingListInfo', self.context)
        assert retval, 'Cound not create the MailingListInfo instance '\
                       'from "%s"' % self.context
        return retval

    @Lazy
    def toAddress(self):
        address = self.mailingListInfo.get_property('mailto')
        n = self.h(self.groupInfo.name)
        retval = formataddr((n, address))
        return retval

    @Lazy
    def rawFromAddress(self):
        retval = self.mailingListInfo.get_property('mailto')
        return retval

    @Lazy
    def fromAddress(self):
        n = self.h(self.groupInfo.name)
        retval = formataddr((n, self.rawFromAddress))
        return retval

    @staticmethod
    def h(h):
        '''Turn the text into a nice header string

:param str h: The string to turn into a header
:returns: The string converted into a UTF-8 encoded header-string
:rtype: str'''
        retval = str(Header(h, utf8))
        assert retval
        return retval

    def add_headers(self, container):
        '''Add the stadard headers to the message

:param container: The email message container to add the headers to.
:type container: email.mime.multipart.MIMEMultipart
:returns: The container (message).

The following headers are added

* :mailheader:`Subject`: The subject set during initialisation
* :mailheader:`From`: the group email address
* :mailheader:`To`: the group email address
* :mailheader:`Sender`: the support email address
* :mailheader:`Precedence`: ``bulk``
* :mailheader:`Organization`: the site name
* :mailheader:`User-Agent`: Identifies GroupServer and this module
* :mailheader:`List-Post`: the group email address
* :mailheader:`List-Unsubscribe`: The unsubscribe ``mailto`` for the group
* :mailheader:`List-Archive`: the address for the group page
* :mailheader:`List-Help`: the address for the help page
* :mailheader:`List-Owner`: the support email address
* :mailheader:`List-ID`: The unique identifier for the group
'''
        # Required headers
        container['Subject'] = self.h(self.subject)
        container['From'] = self.fromAddress
        container['To'] = self.toAddress
        # Sender?
        s = formataddr((self.h('{0} Support'.format(self.siteInfo.name)),
                        self.siteInfo.get_support_email()))
        container['Sender'] = s
        # Nice-to-have headers
        container['Precedence'] = b'Bulk'
        container['Organization'] = self.h(self.siteInfo.name)
        # User-Agent is not actually a real header, but Mozilla and MS use
        # it.
        brag = 'GroupServer  <http://groupserver.org/> '\
               '(gs.groups.messages.digest.base)'
        container['User-Agent'] = self.h(brag)

        # RFC2369 headers: <http://tools.ietf.org/html/rfc2369>
        try:
            p = '<mailto:{0}>'.format(self.rawFromAddress)
            container['List-Post'] = self.h(p)

            u = '<mailto:{0}?Subject=Unsubscribe>'.format(
                self.rawFromAddress)
            container['List-Unsubscribe'] = self.h(u)

            a = '<{0}>'.format(self.groupInfo.url)
            container['List-Archive'] = self.h(a)

            helpS = '<{0}/help> (Help)'.format(self.siteInfo.url)
            container['List-Help'] = self.h(helpS)

            s = '<mailto:{0}>'.format(self.siteInfo.get_support_email())
            container['List-Owner'] = self.h(s)

            # List-ID <http://tools.ietf.org/html/rfc2919>
            canonicalHost = urlparse(self.siteInfo.url).netloc
            gid = '{groupInfo.name} '\
                '<{groupInfo.id}.{canonicalHost}>'.format(
                    groupInfo=self.groupInfo, canonicalHost=canonicalHost)
            container['List-ID'] = gid
        except UnicodeDecodeError:
            # FIXME: Sometimes data is just too messed up.
            # http://farmdev.com/talks/unicode/
            pass
        return container

    def as_string(self):
        '''Represent the email message as a string

:returns: The email message ready for sending.
:rtype: str

The message is a :mimetype:`multipart/alternative` email, with the
plain-text and HTML components of the message are encoded as UTF-8 and added
to the message. The headers are set by
:meth:`.message.Message.add_headers`.'''
        # Stolen from gs.profile.notify.sender.MessageSender
        container = MIMEMultipart('alternative')
        container = self.add_headers(container)

        # Construct the body
        text = MIMEText(self.text.encode(utf8), 'plain', utf8)
        container.attach(text)
        html = MIMEText(self.html.encode(utf8), 'html', utf8)
        container.attach(html)

        retval = container.as_string()
        assert retval
        return retval

    def __str__(self):
        '''See :meth:`.message.Message.as_string`'''
        retval = self.as_string()
        return retval
