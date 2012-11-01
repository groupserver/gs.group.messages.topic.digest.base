# coding=utf-8
from zope.component import createObject
from Products.XWFCore.XWFUtils import date_format_by_age, change_timezone
from gs.viewlet.viewlet import SiteViewlet
from topicsDigest import TopicsDigest

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest')

# Classes used with viewlets. These classes prepare topic digest content for
# rendering. topicsDigest.TopicsDigest does the work of retrieving the content.

class TopicsDigestViewlet(SiteViewlet):
    """ Base Topics Digest class. Common code goes here. Not all that useful
        by itself."""

    def __init__(self, context, request, view, manager):
        SiteViewlet.__init__(self, context, request, view, manager)

        self.siteInfo = view.siteInfo
        self.groupInfo = createObject('groupserver.GroupInfo', context)
        self.groupTz = self.groupInfo.get_property('group_tz', 'UTC')

        self.__topicsDigest = None


    def __buildCommonTopicDigest__(self, topic):
        assert hasattr(self, 'subject_key')

        topicDigest = {
            'subjectLine' : topic[self.subject_key],
            'linkLine' : u'%s/r/topic/%s' % (self.siteInfo.url,
                                                topic['last_post_id']),
            'lastPostAuthor' : topic['lastAuthor'],
            'lastPostDate' : topic['lastPostDate']
            }

        return topicDigest

    def __buildTopicDigest__(self, topic):
        return self.__buildCommonTopicDigest__(topic)

    @property
    def topics(self):
        """ Provides the content of the topics digest. """

        assert hasattr(self, 'frequency')

        if self.__topicsDigest == None:
            self.__topicsDigest = TopicsDigest(self.context, self.siteInfo, self.frequency)

        return self.__topicsDigest.topics

    def topicsDigest(self):
        """ Returns the topics digest. Must be called by a subclass."""

        assert hasattr(self, 'frequency')
        assert hasattr(self, 'last_author_key')

        topics = self.topics
        digest = []

        for topic in topics:
            topic['lastAuthor'] = createObject('groupserver.UserFromId',
                                        self.context,
                                        topic[self.last_author_key])
            dt = change_timezone(topic['last_post_date'], self.groupTz)
            topic['lastPostDate'] = dt.strftime(date_format_by_age(dt))

            digest.append(self.__buildTopicDigest__(topic))

        return digest

class DailyTopicsDigestViewlet(TopicsDigestViewlet):
    """ Viewlet used to pull data for daily topics digests. """

    def __init__(self, context, request, view, manager):
        TopicsDigestViewlet.__init__(self, context, request, view, manager)

        self.__dailyDigestQuery = None
        self.frequency = 'daily'
        self.last_author_key = 'last_author_id'
        self.subject_key = 'original_subject'

    def __buildTopicDigest__(self, topic):
        topicDigest = self.__buildCommonTopicDigest__(topic)
        topicDigest['numPostsToday'] = topic['num_posts_day']
        topicDigest['numPostsTotal'] = topic['num_posts']
        return topicDigest   

class WeeklyTopicsDigestViewlet(TopicsDigestViewlet):
    """ Viewlet used to pull data for weekly topics digests. """
        
    def __init__(self, context, request, view, manager):
        TopicsDigestViewlet.__init__(self, context, request, view, manager)

        self.__weeklyDigestQuery = None
        self.frequency = 'weekly'
        self.last_author_key = 'last_post_user_id'
        self.subject_key = 'subject'
