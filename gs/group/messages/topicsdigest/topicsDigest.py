# coding=utf-8
from zope.component import createObject

from Products.GSSearch.queries import DigestQuery

class TopicsDigest(object):
    """ Data object that represents the content of a topics digest and 
        retrieves that content. """

    def __init__(self, context, siteInfo, freqency='daily'):
        """ freqency: Defaults to 'daily'. Providing 'weekly' will turn the 
            TopicsDigest into a weekly digest. Any other value will turn the
            TopicsDigest into a daily digest."""
        #wpb: I will not be upset if somebody changes the freqency parameter,
        # cause I am not super happy with how it is handled now (especially
        # handling of unaccepted values and defining of accepted values.)

        self.context = context
        self.siteInfo = siteInfo
        self.freqency = 'weekly' if freqency == 'weekly' else 'daily'

        self.groupInfo = createObject('groupserver.GroupInfo', self.context)
        self.groupTz = self.groupInfo.get_property('group_tz', 'UTC')

        self.messageQuery = DigestQuery(context)
        self.__dailyDigestQuery = self.__weeklyDigestQuery = None

    def __dailyTopics__(self):
        
        if self.__dailyDigestQuery == None:
            self.__dailyDigestQuery = \
                self.messageQuery.topics_sinse_yesterday(
                    self.siteInfo.id, [self.groupInfo.id])

        retval = self.__dailyDigestQuery
        assert type(retval) == list
        return retval

    def __weeklyTopics__(self):
        
        if self.__weeklyDigestQuery == None:
            searchTokens = createObject('groupserver.SearchTextTokens',
                self.context)
            searchTokens.set_search_text(u'')
            self.__weeklyDigestQuery = \
                self.messageQuery.topic_search_keyword(searchTokens,
                    self.siteInfo.id, [self.groupInfo.id], limit=7,
                    offset=0, use_cache=True)

        retval = self.__weeklyDigestQuery
        assert type(retval) == list
        return retval


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
            Contents are dependent on the TopicsDigest's frequency attribute.
            The list of returned items only provide data, and should be 
            formatted by a viewlet before being displayed."""
        
        if self.freqency == 'daily':
            retval = self.__dailyTopics__()
        else:
            retval = self.__weeklyTopics__()

        assert type(retval) == list
        return retval
