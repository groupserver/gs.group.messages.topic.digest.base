# coding=utf-8
from datetime import datetime, timedelta
import pytz
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.XWFCore.XWFUtils import date_format_by_age, change_timezone
from queries import DigestQuery

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.topicsdigest')


class BaseTopicsDigest(object):
    """ Data object that represents the content of a topics digest and
        retrieves that content from the database.

        Not meant to be directly created. Instead, a subclass must be created.
        """

    def __init__(self, context, siteInfo):
        self.context = context
        self.siteInfo = siteInfo
        self.__topics = None

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        return retval

    @Lazy
    def groupTz(self):
        retval = self.groupInfo.get_property('group_tz', 'UTC')
        return retval

    @Lazy
    def messageQuery(self):
        retval = DigestQuery()
        return retval

    def __formatTopic__(self, topic):
        # Adds a few fields, and establishes a common set of topic attributes

        assert hasattr(self, '__last_author_key__')
        assert hasattr(self, '__subject_key__')

        # Add a couple of useful attributes
        topic['last_post_author'] = createObject('groupserver.UserFromId',
                                    self.context,
                                    topic[self.__last_author_key__])
        topic['topic_url'] = u'%s/r/topic/%s' % (self.siteInfo.url,
                                                topic['last_post_id'])

        # Fix time
        dt = change_timezone(topic['last_post_date'], self.groupTz)
        topic['last_post_date_str'] = dt.strftime(date_format_by_age(dt))

        # Change names and remove redundent information
        topic['topic_subject'] = topic[self.__subject_key__]
        del topic[self.__subject_key__]
        del topic[self.__last_author_key__]

        return topic

    @property
    def show_digest(self):
        """ Returns a boolean indicating whether the digest should be shown (or
             sent). Subclasses should override based on the relevant criteria
            for making this decision"""
        return True

    @property
    def post_stats(self):
        """ A simple dict providing the following statistical info about the
            topic digest:
                new_topics - Number of new topics in the digest
                existing_topics - Number of topics in the digest that already
                                  existed
                new_posts - Total number of new posts in the digest
        """

        retval = {'new_topics': 0,
                  'existing_topics': 0,
                  'new_posts': 0}
        for topic in self.topics:
            numPostsToday = topic.get('num_posts_today', 0)
            if numPostsToday and (numPostsToday == topic['num_posts_total']):
                retval['new_topics'] = retval['new_topics'] + 1
            else:
                retval['existing_topics'] = retval['existing_topics'] + 1
            retval['new_posts'] = retval['new_posts'] + numPostsToday
        assert type(retval) == dict, 'Not a dict'
        assert 'new_topics' in retval.keys()
        assert 'existing_topics' in retval.keys()
        assert 'new_posts' in retval.keys()
        return retval

    @property
    def topics(self):
        """ Provides a list of the individual items that are part of a digest.
            Each item is a dict that provides the following attributes about
            a topic:
                topic_subject - The subject/title of the topic
                topic_url - URL to view the topic
                last_post_author - An IGSUserInfo implementation representing
                                   the last user to post in the topic
                last_post_date - Datetime of the last post in the topic, as
                                 provided by the database
                last_post_date_str -  Date and time of the last post in the
                                      topic, as a string, adjusted for the
                                      timezone of the group
                last_post_id - ID string of the last post in in the topic

            Subclasses of BaseTopicsDigest may provide additional attributes.
        """

        assert hasattr(self, '__getTopics__')

        if self.__topics is None:
            self.__topics = self.__getTopics__()
            self.__topics = [self.__formatTopic__(topic)
                                for topic in self.__topics]
        retval = self.__topics
        assert isinstance(retval, list)
        return retval


class DailyTopicsDigest(BaseTopicsDigest):
    """ Represents the content of a daily digest.

        Dicts in the list provided by topics include the following attributes,
        in addition to the standard attributes:
            num_posts_today - Number of posts made in the topic today
            num_posts_total - Total number of posts in the topic
        """

    def __init__(self, context, siteInfo):
        super(DailyTopicsDigest, self).__init__(context, siteInfo)
        self.__dailyDigestQuery__ = None
        self.__last_author_key__ = 'last_author_id'
        self.__subject_key__ = 'subject'

    def __getTopics__(self):
        if self.__dailyDigestQuery__ is None:
            self.__dailyDigestQuery__ = \
                self.messageQuery.topics_sinse_yesterday(self.siteInfo.id,
                                                            self.groupInfo.id)

        retval = self.__dailyDigestQuery__
        assert type(retval) == list
        return retval

    def __formatTopic__(self, topic):
        topic = super(DailyTopicsDigest, self).__formatTopic__(topic)
        topic['num_posts_today'] = topic['num_posts_day']
        topic['num_posts_total'] = topic['num_posts']
        del topic['num_posts_day']
        del topic['num_posts']
        return topic

    @Lazy
    def show_digest(self):
        """ True if there has been a post made in the group in the previous
            24 hours."""
        retval = (self.post_stats['new_posts'] > 0)
        assert type(retval) == bool
        return retval


class WeeklyTopicsDigest(BaseTopicsDigest):
    """ Represents the content of a weekly digest."""

    def __init__(self, context, siteInfo):
        super(WeeklyTopicsDigest, self).__init__(context, siteInfo)
        self.__weeklyDigestQuery__ = None
        self.__last_author_key__ = 'last_post_user_id'
        self.__subject_key__ = 'subject'
        self.frequency = 7

    def __getTopics__(self):

        if self.__weeklyDigestQuery__ is None:
            self.__weeklyDigestQuery__ = \
                self.messageQuery.recent(self.siteInfo.id, self.groupInfo.id,
                                            limit=7, offset=0)

        retval = self.__weeklyDigestQuery__
        assert type(retval) == list
        return retval

    @Lazy
    def show_digest(self):
        """ True if there are posts in the group, the most recent post is
            not from today, and today is the weekly anniversary of the most
            recent post in the group."""
        time_since_last_post = timedelta(0)
        if self.post_stats['existing_topics'] != 0:
            time_since_last_post = datetime.now(pytz.UTC) - \
                                    self.topics[0]['last_post_date']
                                                
        log.info("Days since last post: %d" % time_since_last_post.days)
        retval = ((self.post_stats['existing_topics'] != 0) and
                  (time_since_last_post.days != 0) and
                  (time_since_last_post.days % self.frequency == 0))
        assert type(retval) == bool
        return retval
