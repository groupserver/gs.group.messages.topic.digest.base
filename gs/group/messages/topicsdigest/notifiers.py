# coding=utf-8
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
# TODO Create and use a MessageSender made for notifying groups
from gs.profile.notify.sender import MessageSender
from Products.XWFMailingListManager.queries import DigestQuery
from topicsDigest import TopicsDigest
UTF8 = 'utf-8'

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.notifiers')

class TopicsDigestNotifier(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.siteInfo = createObject('groupserver.SiteInfo', self.context)

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        assert retval, 'Could not create the GroupInfo from %s' % self.context
        return retval

    @Lazy
    def mailingListInfo(self):
        retval = createObject('groupserver.MailingListInfo', self.context)
        assert retval, 'Cound not create the MailingListInfo instance from %s' % self.context
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

    @property
    def subject(self):
        digestStats = self.topicsDigest.post_stats
        subject = { 'groupShortName' : self.groupInfo.get_property('short_name', self.groupInfo.name), 
            'newPosts' : digestStats['newPosts'], 
            'newTopics' : digestStats['newTopics']
            }
        return '%(groupShortName)s Topic Digest: %(newPosts)d New Posts, %(newTopics)d New Topics' % subject

    def notify(self):
        
        digestQuery = DigestQuery(self.context)

	    # check to see if we have a digest in the last day, and if so, shortcut
        if digestQuery.has_digest_since(self.siteInfo.id, self.groupInfo.get_id()):
            m = u'%s (%s) on %s (%s): Have already issued digest in last day' % \
              (self.groupInfo.name, self.groupInfo.id, self.siteInfo.name, self.siteInfo.id)
            log.info(m)
            return


        subject = self.subject
        text = self.textTemplate(topics=self.topicsDigest.topics)
        html = self.htmlTemplate(topics=self.topicsDigest.topics)
        # Getting those group members who are subscribed via digest.
        # TODO There MUST be a more elegant way to do this. Find it.
        digestMemberAddresses = createObject('groupserver.MailingListInfo', self.context).mlist.getValueFor('digestmaillist')
        for address in digestMemberAddresses:
            userId = self.context.site_root().acl_users.get_userByEmail(address.lower()).id
            user = createObject('groupserver.UserFromId', self.context, userId)
            ms = MessageSender(self.context, user)
            ms.send_message(subject, text, html)

        digestQuery.update_group_digest(self.siteInfo.id, self.groupInfo.get_id())


class DailyTopicsDigestNotifier(TopicsDigestNotifier):
    textTemplateName = 'gs-group-messages-topicsdigest-daily.txt'
    htmlTemplateName = 'gs-group-messages-topicsdigest-daily.html'

    def __init__(self, context, request):
        TopicsDigestNotifier.__init__(self, context, request)
        self.topicsDigest = TopicsDigest(self.context, self.siteInfo, 'daily')

    
class WeeklyTopicsDigestNotifier(TopicsDigestNotifier):
    textTemplateName = 'gs-group-messages-topicsdigest-weekly.txt'
    htmlTemplateName = 'gs-group-messages-topicsdigest-weekly.html'

    def __init__(self, context, request):
        TopicsDigestNotifier.__init__(self, context, request)
        self.topicsDigest = TopicsDigest(self.context, self.siteInfo, 'weekly')

