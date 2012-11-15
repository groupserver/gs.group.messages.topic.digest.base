# coding=utf-8
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
# TODO Create and use a MessageSender made for notifying groups
from gs.profile.notify.sender import MessageSender
from topicsDigest import TopicsDigest
UTF8 = 'utf-8'

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
            'newPosts' : digestStats.newPosts, 
            'newTopics' : digestStats.newTopics
            }
        return '%(groupShortName)s Topic Digest: %(newPosts)n New Posts, %(newTopics)n New Topics' % subject

    def notify(self):
        subject = self.subject
        text = self.textTemplate(topics=self.topicsDigest.topics)
        html = self.htmlTemplate(topics=self.topicsDigest.topics)
        allusers = self.groupInfo.group_members_info.fullMembers
        for user in allusers:
            ms = MessageSender(self.context, user)
            ms.send_message(subject, text, html)


class DailyTopicsDigestNotifier(TopicsDigestNotifier):
    textTemplateName = 'gs-group-messages-topicsdigest-daily.txt'
    htmlTemplate = 'gs-group-messages-topicsdigest-daily.html'

    def __init__(self, context, request):
        TopicsDigestNotifier.__init__(self, context, request)
        self.topicsDigest = TopicsDigest(self.context, self.siteInfo, 'daily')

    
class WeeklyTopicsDigestNotifier(TopicsDigestNotifiers):
    textTemplateName = 'gs-group-messages-topicsdigest-weekly.txt'
    htmlTemplate = 'gs-group-messages-topicsdigest-weekly.html'

    def __init__(self, context, request)
        TopicsDigestNotifier.__init__(self, context, request)
        self.topicsDigest = TopicsDigest(self.context, self.siteInfo, 'weekly')

