# coding=utf-8
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
from gs.email import send_email
from topicsDigest import DailyTopicsDigest, WeeklyTopicsDigest
from message import Message
from queries import SendQuery
UTF8 = 'utf-8'

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.notifiers')


class DynamicTopicsDigestNotifier(object):

    def __init__(self, group, request):
        self.context = self.group = group
        self.request = request

    @Lazy
    def topicsDigest(self):
        retval = DailyTopicsDigest(self.context, self.siteInfo)
        if not retval.show_digest:
            retval = WeeklyTopicsDigest(self.context, self.siteInfo)
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.group)
        return retval

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.group)
        assert retval, 'Could not create the GroupInfo from %s' % self.group
        return retval

    @Lazy
    def sendQuery(self):
        retval = SendQuery()
        return retval

    @Lazy
    def daily(self):
        'Returns True if we should send a daily digest'
        retval = self.sendQuery.has_digest_since(self.siteInfo.id,
                                                    self.groupInfo.id)
        return retval

    @Lazy
    def baseTemplate(self):
        period = 'daily' if self.daily else 'weekly'
        retval = 'gs-group-messages-topicsdigest-{0}'.format(period)
        return retval

    @Lazy
    def textTemplate(self):
        templateName = '{0}.txt'.format(self.baseTemplate)
        retval = getMultiAdapter((self.group, self.request), name=templateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        templateName = '{0}.html'.format(self.baseTemplate)
        retval = getMultiAdapter((self.group, self.request), name=templateName)
        assert retval
        return retval

    @Lazy
    def subject(self):
        m = '{groupShortName} Topic Digest: {new_posts} New Posts, '\
            '{new_topics} New Topics'
        shortName = self.groupInfo.get_property('short_name',
                                                self.groupInfo.name)
        digestStats = self.topicsDigest.post_stats
        retval = m.format(groupShortName=shortName,
                          new_posts=digestStats['new_posts'],
                          new_topics=digestStats['new_topics'])
        assert retval
        return retval

    @Lazy
    def digestMemberAddresses(self):
        '''Those group members who are subscribed via digest.'''
        mListInfo = createObject('groupserver.MailingListInfo', self.group)
        mlist = mListInfo .mlist
        rawList = mlist.getValueFor('digestmaillist') or []

        site_root = self.context.site_root()
        acl_users = site_root.acl_users
        # Only return real addresses for real users
        retval = [a for a in rawList
                    if (('@' in a)
                        and acl_users.get_userIdByEmail(a.lower()))]
        assert type(retval) == list
        return retval

    def notify(self):
        """
        Creates the text and html bodies of an digest email (using template
        names defined by subclasses) and the subject line of a digest email
        based on information retrieved from the database. Then sends the digest
        email to members of the group who are subscribed to topics digests, it
        the information from the database indicates that a digest should be
        sent.

        A digest log is also checked and modified. If the log shows that a
        digest has been sent to the group in the previous 24 hours, a digest
        will not be created and sent. If a digest is created and sent, the log
        will be updated to reflect when the digest emails were sent.
        """
        if (self.daily
            or ((not self.daily) and self.topicsDigest.show_digest)):
            text = self.textTemplate(topicsDigest=self.topicsDigest)
            html = self.htmlTemplate(topicsDigest=self.topicsDigest)
            message = Message(self.group)
            messageString = message.create_message(self.subject, text, html)
            send_email(message.rawFromAddress, self.digestMemberAddresses,
                        messageString)
            self.sendQuery.update_group_digest(self.siteInfo.id,
                                                self.groupInfo.id)

            m = 'Sent digest from {0} on {1} to {2} address.'
            msg = m.format(self.groupInfo.id, self.siteInfo.id,
                            len(self.digestMemberAddresses))
            log.info(msg)
