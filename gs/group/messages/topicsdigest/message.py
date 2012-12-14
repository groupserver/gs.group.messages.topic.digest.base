# -*- coding: utf-8 -*-
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
        retval = formataddr((self.groupInfo.name.encode(utf8), address))
        return retval

    @Lazy
    def rawFromAddress(self):
        retval = self.mailingListInfo.get_property('mailto')
        return retval

    @Lazy
    def fromAddress(self):
        retval = formataddr((self.groupInfo.name.encode(utf8),
                                self.rawFromAddress))
        return retval

    def h(self, h):
        'Turn the text h into a nice header string'
        retval = str(Header(h, utf8))
        return retval

    def create_message(self, subject, txtMessage, htmlMessage):
        # Stolen from gs.profile.notify.sender.MessageSender
        container = MIMEMultipart('alternative')
        # Required headers
        container['Subject'] = self.h(subject)
        container['From'] = self.fromAddress
        container['To'] = self.toAddress
        # Nice-to-have headers
        container['Precedence'] = self.h('Bulk')
        container['Organization'] = self.h(self.siteInfo.name)
        # User-Agent is not actually a real header, but Mozilla and MS use it.
        brag = 'GroupServer (gs.groups.messages.topicsdigest)'
        container['User-Agent'] = self.h(brag)

        # RFC2369 headers: <http://tools.ietf.org/html/rfc2369>
        p = '<mailto:{0}>'.format(self.rawFromAddress)
        container['List-Post'] = self.h(p)

        u = '<mailto:{0}?Subject=Unsubscribe>'.format(self.rawFromAddress)
        container['List-Unsubscribe'] = self.h(u)

        a = '<{0}> (Archive of {1})'.format(self.groupInfo.url,
                                            self.groupInfo.name)
        container['List-Archive'] = self.h(a)

        helpS = '<{0}/help> (Help)'.format(self.siteInfo.url)
        container['List-Help'] = self.h(helpS)

        s = '<mailto:{0}> ({1} Support)'.format(
                self.siteInfo.get_support_email(), self.siteInfo.name)
        container['List-Owner'] = self.h(s)

        # Construct the body
        txt = MIMEText(txtMessage.encode(utf8), 'plain', utf8)
        container.attach(txt)
        html = MIMEText(htmlMessage.encode(utf8), 'html', utf8)
        container.attach(html)

        retval = container.as_string()
        assert retval
        return retval
