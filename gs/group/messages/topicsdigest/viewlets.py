# coding=utf-8
from zope.component import createObject
from Products.XWFCore.XWFUtils import date_format_by_age, change_timezone
from gs.viewlet.viewlet import SiteViewlet
from topicsDigest import DailyTopicsDigest, WeeklyTopicsDigest

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest')

# Viewlet classes (duh). These classes prepare topic digest content for
# rendering. TopicsDigest does the work of retrieving the content.

class HeaderFooterViewlet(SiteViewlet):
    """ Convientently provides basic info for the header and footer"""

    def __init__(self, context, request, view, manager):
        SiteViewlet.__init__(self, context, request, view, manager)

        self.siteInfo = view.siteInfo
        self.groupInfo = createObject('groupserver.GroupInfo', context)
        self.emailDomain = getattr(self.context, 'GlobalConfiguration', None).getProperty('emailDomain')
        self.groupEmail = '%s@%s' % (self.groupInfo.get_id(), self.emailDomain)

class TopicsDigestViewlet(SiteViewlet):
    """ Base Topics Digest class. Common code goes here. Not all that useful
        by itself."""

    def __init__(self, context, request, view, manager):
        SiteViewlet.__init__(self, context, request, view, manager)

        self.siteInfo = view.siteInfo
        self.groupInfo = createObject('groupserver.GroupInfo', context)
        self.groupTz = self.groupInfo.get_property('group_tz', 'UTC')

    def __buildCommonFormattedTopic__(self, topic):
        assert hasattr(self, 'subject_key')

        formattedTopic = {
            'subjectLine' : topic[self.subject_key],
            'topicUrl' : u'%s/r/topic/%s' % (self.siteInfo.url,
                                                topic['last_post_id']),
            'lastPostAuthor' : topic['lastAuthor'],
            'lastPostDate' : topic['lastPostDate']
            }

        return formattedTopic

    def __buildFormattedTopic__(self, topic):
        return self.__buildCommonFormattedTopic__(topic)

    @property
    def topics(self):
        """ Provides the list of topic models in the current digest."""
        assert hasattr(self, '__topicsDigest__')
        retval = self.__topicsDigest__.topics
        assert isinstance(retval, list)
        return retval 

    def formatTopic(self, topic):
        """ Does the formatting needed to make the models of a topic digest
            displayable."""

        assert hasattr(self, 'last_author_key')

        topic['lastAuthor'] = createObject('groupserver.UserFromId',
                                    self.context,
                                    topic[self.last_author_key])
        dt = change_timezone(topic['last_post_date'], self.groupTz)
        topic['lastPostDate'] = dt.strftime(date_format_by_age(dt))

        return self.__buildFormattedTopic__(topic)

class DailyTopicsDigestViewlet(TopicsDigestViewlet):
    """ Viewlet used to pull data for daily topics digests. """

    def __init__(self, context, request, view, manager):
        TopicsDigestViewlet.__init__(self, context, request, view, manager)

        self.__topicsDigest__ = DailyTopicsDigest(self.context, self.siteInfo)
        self.last_author_key = 'last_author_id'
        self.subject_key = 'original_subject'

    def __buildFormattedTopic__(self, topic):
        formattedTopic = self.__buildCommonFormattedTopic__(topic)
        formattedTopic['numPostsToday'] = topic['num_posts_day']
        formattedTopic['numPostsTotal'] = topic['num_posts']
        return formattedTopic   

class WeeklyTopicsDigestViewlet(TopicsDigestViewlet):
    """ Viewlet used to pull data for weekly topics digests. """
        
    def __init__(self, context, request, view, manager):
        TopicsDigestViewlet.__init__(self, context, request, view, manager)
        
        self.__topicsDigest__ = WeeklyTopicsDigest(self.context, self.siteInfo)
        self.last_author_key = 'last_post_user_id'
        self.subject_key = 'subject'
