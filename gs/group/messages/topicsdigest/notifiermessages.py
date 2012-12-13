# coding=utf-8
from zope.component import getMultiAdapter
from zope.cachedescriptors.property import Lazy
from gs.group.base.page import GroupPage
from topicsDigest import DailyTopicsDigest, WeeklyTopicsDigest

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.notifiermessages')

# Classes used with page templates


class TopicsDigestMessage(GroupPage):
    pass


class TopicsDigestMessageText(TopicsDigestMessage):
    def __init__(self, context, request):
        TopicsDigestMessage.__init__(self, context, request)
        response = request.response
        response.setHeader("Content-Type", "text/plain; charset=UTF-8")


class DynamicTopicsDigestMixin(object):

    @Lazy
    def dailyTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                    name=self.dailyTemplateName)
        assert retval
        return retval

    @Lazy
    def weeklyTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                    name=self.weeklyTemplateName)
        assert retval
        return retval

    def __call__(self, topicsDigest=None):
        self.topicsDigest = topicsDigest if topicsDigest is not None \
                else DailyTopicsDigest(self.context, self.siteInfo)
        if isinstance(self.topicsDigest, DailyTopicsDigest):
            if self.topicsDigest.post_stats['new_posts'] > 0:
                self.output = \
                    self.dailyTemplate(topicsDigest=self.topicsDigest)
            else:
                self.topicsDigest = \
                    WeeklyTopicsDigest(self.context, self.siteInfo)

        if isinstance(self.topicsDigest, WeeklyTopicsDigest):
            self.output = self.weeklyTemplate(topicsDigest=self.topicsDigest)

        retval = self.output
        return retval


class DynamicTopicsDigestMessage(TopicsDigestMessage,
                                    DynamicTopicsDigestMixin):
    dailyTemplateName = 'gs-group-messages-topicsdigest-daily.html'
    weeklyTemplateName = 'gs-group-messages-topicsdigest-weekly.html'

    def __init__(self, context, request):
        TopicsDigestMessage.__init__(self, context, request)


class DynamicTopicsDigestMessageText(TopicsDigestMessageText,
                                        DynamicTopicsDigestMixin):
    dailyTemplateName = 'gs-group-messages-topicsdigest-daily.txt'
    weeklyTemplateName = 'gs-group-messages-topicsdigest-weekly.txt'

    def __init__(self, context, request, topicsDigest=None):
        TopicsDigestMessage.__init__(self, context, request)
