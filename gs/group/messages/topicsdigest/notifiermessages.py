# coding=utf-8
'''The classes used with the page templates'''
from zope.cachedescriptors.property import Lazy
from gs.group.base.page import GroupPage
from topicsDigest import DailyTopicsDigest, WeeklyTopicsDigest
from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.notifiermessages')


class TopicsDigestMessage(GroupPage):
    def __init__(self, context, request):
        super(TopicsDigestMessage, self).__init__(context, request)

    @property
    def digest(self):
        raise NotImplementedError

    def __call__(self, topicsDigest=None):
        digest = self.digest if topicsDigest is None else topicsDigest
        retval = super(TopicsDigestMessage, self).__call__(topicsDigest=digest)
        return retval


class WeeklyMessage(TopicsDigestMessage):
    @Lazy
    def digest(self):
        retval = WeeklyTopicsDigest(self.context, self.siteInfo)
        return retval


class WeeklyMessageText(WeeklyMessage):
    def __call__(self, topicsDigest=None):
        retval = super(WeeklyMessageText, self).__call__(topicsDigest)
        self.request.response.setHeader("Content-Type",
                                        "text/plain; charset=UTF-8")
        return retval


class DailyMessage(TopicsDigestMessage):
    @Lazy
    def digest(self):
        retval = DailyTopicsDigest(self.context, self.siteInfo)
        return retval


class DailyMessageText(DailyMessage):
    def __call__(self, topicsDigest=None):
        retval = super(DailyMessageText, self).__call__(topicsDigest)
        self.request.response.setHeader("Content-Type",
                                        "text/plain; charset=UTF-8")
        return retval
