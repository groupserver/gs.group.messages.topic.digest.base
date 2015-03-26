# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from logging import getLogger
log = getLogger('gs.group.messages.topic.digest.base.topicsdigest')
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.XWFCore.XWFUtils import date_format_by_age, change_timezone
from .queries import DigestQuery


class BaseTopicsDigest(object):
    """ Data object that represents the content of a topics digest and
retrieves that content from the database.

Not meant to be directly created. Instead, a subclass must be created.
"""

    def __init__(self, context, siteInfo):
        self.context = context
        self.siteInfo = siteInfo
        self.topicsList = None

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        return retval

    @Lazy
    def groupTz(self):
        retval = self.groupInfo.get_property(b'group_tz', 'UTC')
        return retval

    @Lazy
    def messageQuery(self):
        retval = DigestQuery()
        return retval

    def format_topic(self, topic):
        # Adds a few fields, and establishes a common set of topic
        # attributes

        assert hasattr(self, 'last_author_key')
        assert hasattr(self, 'subject_key')

        # Add a couple of useful attributes
        topic['last_post_author'] = createObject(
            'groupserver.UserFromId', self.context,
            topic[self.last_author_key])
        u = u'{0}/r/topic/{1}'
        topic['topic_url'] = u.format(self.siteInfo.url,
                                      topic['last_post_id'])

        # Fix time
        dt = change_timezone(topic['last_post_date'], self.groupTz)
        topic['last_post_date_str'] = dt.strftime(date_format_by_age(dt))

        # Change names and remove redundent information
        topic['topic_subject'] = topic[self.subject_key]
        del topic[self.subject_key]
        del topic[self.last_author_key]
        return topic

    @property
    def show_digest(self):
        """A boolean indicating whether the digest should be shown
(or sent).

Subclasses should override based on the relevant criteria for making this
decision"""
        return True

    @property
    def post_stats(self):
        """A simple dict providing the following statistical info about the
topic digest:

``new_topics``:

    Number of new topics in the digest

``existing_topics``:

    Number of topics in the digest that already existed

``new_posts``:

    Total number of new posts in the digest"""

        retval = {'new_topics': 0,
                  'existing_topics': 0,
                  'new_posts': 0}
        for topic in self.topics:
            numPostsToday = topic.get('num_posts_today', 0)
            if (numPostsToday and
               (numPostsToday == topic['num_posts_total'])):
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
        """A list of the individual items that are part of a digest.

Each item is a dict that provides the following attributes about a topic:

``topic_subject``:

    The subject/title of the topic

``topic_url``:

    URL to view the topic

``last_post_author``:

    An IGSUserInfo implementation representing the last user to post in the
    topic

``last_post_date``:

    Datetime of the last post in the topic, as provided by the database


``last_post_date_str``:

    Date and time of the last post in the topic, as a string, adjusted for
    the timezone of the group

``last_post_id``:

    ID string of the last post in in the topic

Subclasses of :class:`BaseTopicsDigest` may provide additional
attributes."""

        assert hasattr(self, 'get_topics')

        if self.topicsList is None:
            self.topicsList = [self.format_topic(topic)
                               for topic in self.get_topics()]
        retval = self.topicsList
        assert isinstance(retval, list)
        return retval
