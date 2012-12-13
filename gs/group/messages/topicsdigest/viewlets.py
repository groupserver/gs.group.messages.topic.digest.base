# coding=utf-8
from zope.component import createObject
from gs.viewlet.viewlet import SiteViewlet
from topicsDigest import DailyTopicsDigest, WeeklyTopicsDigest

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest')


class HeaderFooterViewlet(SiteViewlet):
    """ Convientently provides basic info for the header and footer"""

    def __init__(self, context, request, view, manager):
        SiteViewlet.__init__(self, context, request, view, manager)

        self.siteInfo = view.siteInfo
        self.groupInfo = createObject('groupserver.GroupInfo', context)
        config = getattr(self.context, 'GlobalConfiguration')
        self.emailDomain = config.getProperty('emailDomain')
        self.groupEmail = '%s@%s' % (self.groupInfo.get_id(), self.emailDomain)


class TopicsDigestViewlet(SiteViewlet):
    """ Base Topics Digest class. Common code goes here. Not all that useful
        by itself."""

    def __init__(self, context, request, view, manager):
        SiteViewlet.__init__(self, context, request, view, manager)

        self.siteInfo = view.siteInfo
        self.groupInfo = createObject('groupserver.GroupInfo', context)
        self.groupTz = self.groupInfo.get_property('group_tz', 'UTC')

    @property
    def topics(self):
        """ Provides the list of topic models in the current digest."""
        assert hasattr(self, '__topicsDigest__')
        retval = self.__topicsDigest__.topics
        assert isinstance(retval, list)
        return retval


class DailyTopicsDigestViewlet(TopicsDigestViewlet):
    """ Viewlet used to pull data for daily topics digests. """

    def __init__(self, context, request, view, manager):
        TopicsDigestViewlet.__init__(self, context, request, view, manager)

        self.__topicsDigest__ = DailyTopicsDigest(self.context, self.siteInfo)


class WeeklyTopicsDigestViewlet(TopicsDigestViewlet):
    """ Viewlet used to pull data for weekly topics digests. """

    def __init__(self, context, request, view, manager):
        TopicsDigestViewlet.__init__(self, context, request, view, manager)

        self.__topicsDigest__ = WeeklyTopicsDigest(self.context, self.siteInfo)
