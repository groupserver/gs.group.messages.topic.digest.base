# coding=utf-8
from gs.group.base import GroupViewlet
from topicsDigest import BaseTopicsDigest, DailyTopicsDigest,\
    WeeklyTopicsDigest
from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest')


class HeaderFooterViewlet(GroupViewlet):
    """ Convientently provides basic info for the header and footer"""

    def __init__(self, context, request, view, manager):
        super(HeaderFooterViewlet, self).__init__(context, request, view,
                                                    manager)

        config = getattr(self.context, 'GlobalConfiguration')
        self.emailDomain = config.getProperty('emailDomain')
        self.groupEmail = '%s@%s' % (self.groupInfo.get_id(), self.emailDomain)


class TopicsDigestViewlet(GroupViewlet):
    """ Base Topics Digest class. Common code goes here. Not all that useful
        by itself."""

    def __init__(self, context, request, view, manager):
        super(TopicsDigestViewlet, self).__init__(context, request, view,
                                                    manager)
        self.groupTz = self.groupInfo.get_property('group_tz', 'UTC')

    @property
    def topicsDigest(self):
        """ Provides the list of topic models in the current digest."""
        assert hasattr(self, '__topicsDigest__')
        retval = self.__topicsDigest__
        assert isinstance(retval, BaseTopicsDigest)
        return retval


class DailyTopicsDigestViewlet(TopicsDigestViewlet):
    """ Viewlet used to pull data for daily topics digests. """

    def __init__(self, context, request, view, manager):
        super(DailyTopicsDigestViewlet, self).__init__(context, request, view,
                                                        manager)
        self.__topicsDigest__ = DailyTopicsDigest(self.context, self.siteInfo)


class WeeklyTopicsDigestViewlet(TopicsDigestViewlet):
    """ Viewlet used to pull data for weekly topics digests. """

    def __init__(self, context, request, view, manager):
        super(WeeklyTopicsDigestViewlet, self).__init__(context, request, view,
                                                        manager)
        self.__topicsDigest__ = WeeklyTopicsDigest(self.context, self.siteInfo)
