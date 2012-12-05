# coding=utf-8
from zope.component import createObject

from Products.GSSearch.queries import DigestQuery

class BaseTopicsDigest(object):
    """ Data object that represents the content of a topics digest and 
        retrieves that content. """

    def __init__(self, context, siteInfo):
        self.context = context
        self.siteInfo = siteInfo

        self.groupInfo = createObject('groupserver.GroupInfo', self.context)
        self.groupTz = self.groupInfo.get_property('group_tz', 'UTC')

        self.messageQuery = DigestQuery(context)
        self.__topics = None

    @property
    def post_stats(self):
        retval = {'newTopics': 0,
                  'existingTopics': 0,
                  'newPosts':  0}
        for topic in self.topics:
            numPostsDay = topic.get('num_posts_day', 0)
            if numPostsDay and (numPostsDay == topic['num_posts']):
                retval['newTopics'] = retval['newTopics'] + 1
            else:
                retval['existingTopics'] = retval['existingTopics'] + 1
            retval['newPosts'] = retval['newPosts'] + numPostsDay
        assert type(retval) == dict, 'Not a dict'
        assert 'newTopics'       in retval.keys()
        assert 'existingTopics'  in retval.keys()
        assert 'newPosts'        in retval.keys()
        return retval

    @property
    def topics(self):
        """ Provides a list of the individual items that are part of a digest.
            The list of returned items only provide data, and should be 
            formatted by a viewlet before being displayed."""

        if self.__topics == None:
            self.__topics = self.__getTopics__()
        retval = self.__topics
        assert isinstance(retval, list)
        return retval
        
class DailyTopicsDigest(BaseTopicsDigest):

    def __init__(self, context, siteInfo):
        BaseTopicsDigest.__init__(self, context, siteInfo)
        self.__dailyDigestQuery__ = None

    def __getTopics__(self):
        if self.__dailyDigestQuery__ == None:
            self.__dailyDigestQuery__ = \
                self.messageQuery.topics_sinse_yesterday(
                    self.siteInfo.id, [self.groupInfo.id])

        retval = self.__dailyDigestQuery__
        assert type(retval) == list
        return retval

class WeeklyTopicsDigest(BaseTopicsDigest):
    def __init__(self, context, siteInfo):
        BaseTopicsDigest.__init__(self, context, siteInfo)
        self.__weeklyDigestQuery__ = None

    def __getTopics__(self):
        
        if self.__weeklyDigestQuery__ == None:
            searchTokens = createObject('groupserver.SearchTextTokens',
                self.context)
            searchTokens.set_search_text(u'')
            self.__weeklyDigestQuery__ = \
                self.messageQuery.topic_search_keyword(searchTokens,
                    self.siteInfo.id, [self.groupInfo.id], limit=7,
                    offset=0, use_cache=True)

        retval = self.__weeklyDigestQuery__
        assert type(retval) == list
        return retval
