# coding=utf-8
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
# TODO Create and use a MessageSender made for notifying groups
from gs.profile.notify.sender import MessageSender
from Products.XWFMailingListManager.queries import DigestQuery
from topicsDigest import DailyTopicsDigest, WeeklyTopicsDigest
UTF8 = 'utf-8'

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.notifiers')

class TopicsDigestNotifier(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy 
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
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
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                    name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                    name=self.htmlTemplateName)
        assert retval
        return retval

    @Lazy
    def subject(self):
        m = '{groupShortName} Topic Digest: {newPosts} New Posts, '\
            '{newTopics} New Topics'
        shortName = self.groupInfo.get_property('short_name', 
                                                self.groupInfo.name)
        digestStats = self.topicsDigest.post_stats
        retval = m.format(groupShortName=shortName, 
                          newPosts=digestStats['newPosts'],
                          newTopics=digestStats['newTopics'])
        assert retval
        return retval

    @Lazy
    def acl_users(self):
        site_root = self.context.site_root()
        retval = site_root.acl_users
        return retval

    @Lazy
    def digestMemberAddresses(self):
        '''Those group members who are subscribed via digest.'''
        # TODO There MUST be a more elegant way to do this. Find it.
        mailingListInfo = createObject('groupserver.MailingListInfo', 
                                       self.context)
        mlist = mailingListInfo.mlist
        retval = mlist.getValueFor('digestmaillist') or []
        assert type(retval) == list
        return retval

    def notify(self):
        digestQuery = DigestQuery(self.context)
        # Shortcut if we have sent a digest in the last day
        if digestQuery.has_digest_since(self.siteInfo.id, 
                                        self.groupInfo.get_id()):
            m = u'%s (%s) on %s (%s): Have already issued digest in last '\
                'day' % (self.groupInfo.name, self.groupInfo.id, 
                         self.siteInfo.name, self.siteInfo.id)
            log.info(m)
        else:
            text = self.textTemplate(topicsDigest=self.topicsDigest)
            html = self.htmlTemplate(topicsDigest=self.topicsDigest)
            for address in self.digestMemberAddresses:
                u = self.acl_users.get_userByEmail(address.lower())
                if u:
                    userId = u.getId()
                    user = createObject('groupserver.UserFromId', self.context, 
                                        userId)
                    ms = MessageSender(self.context, user)
                    ms.send_message(self.subject, text, html)
                else:
                    m = 'No user for <{address}>, but listed in {groupId} on '\
                        '{siteId}.'
                    msg = m.format(address=address, groupId=self.groupInfo.id,
                                   siteId=self.siteInfo.id)
                    log.warn(msg)
            digestQuery.update_group_digest(self.siteInfo.id, 
                                            self.groupInfo.id)

class DailyTopicsDigestNotifier(TopicsDigestNotifier):
    textTemplateName = 'gs-group-messages-topicsdigest-daily.txt'
    htmlTemplateName = 'gs-group-messages-topicsdigest-daily.html'

    def __init__(self, context, request):
        TopicsDigestNotifier.__init__(self, context, request)
        self.topicsDigest = DailyTopicsDigest(self.context, self.siteInfo)

    
class WeeklyTopicsDigestNotifier(TopicsDigestNotifier):
    textTemplateName = 'gs-group-messages-topicsdigest-weekly.txt'
    htmlTemplateName = 'gs-group-messages-topicsdigest-weekly.html'

    def __init__(self, context, request):
        TopicsDigestNotifier.__init__(self, context, request)
        self.topicsDigest = WeeklyTopicsDigest(self.context, self.siteInfo)


class DynamicTopicsDigestNotifier(TopicsDigestNotifier):
    textTemplateName = 'gs-group-messages-topicsdigest-dynamic.txt'
    htmlTemplateName = 'gs-group-messages-topicsdigest-dynamic.html'

    def __init__(self, context, request):
        TopicsDigestNotifier.__init__(self, context, request)
        self.topicsDigest = DailyTopicsDigest(self.context, self.siteInfo)
        if self.topicsDigest.post_stats['newPosts'] == 0:
            self.topicsDigest = WeeklyTopicsDigest(self.context, self.siteInfo)
