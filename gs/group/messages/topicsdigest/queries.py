# -*- coding: utf-8 *-*
import datetime
import sqlalchemy as sa
from zope.sqlalchemy import mark_changed
from gs.database import getTable, getSession
from gs.group.messages.topics.queries import TopicsQuery


class SendQuery(object):
    def __init__(self):

        self.digestTable = getTable('group_digest')
        self.now = datetime.datetime.now()

    def has_digest_since(self, site_id, group_id,
                        interval=datetime.timedelta(0.9)):
        """ Have there been any digests sent in the last 'interval' time
        period? (Default 21.6 hours)

        """
        sincetime = self.now - interval
        dt = self.digestTable

        statement = dt.select()

        statement.append_whereclause(dt.c.site_id == site_id)
        statement.append_whereclause(dt.c.group_id == group_id)
        statement.append_whereclause(dt.c.sent_date >= sincetime)

        session = getSession()
        r = session.execute(statement)

        result = False
        if r.rowcount:
            result = True

        return result

    def no_digest_but_active(self, interval='7 days',
                            active_interval='3 months'):
        """ Returns a list of dicts containing site_id and group_id
            which have not received a digest in the 'interval' time period.

        """
        s = sa.text("""SELECT DISTINCT topic.site_id, topic.group_id FROM
  (SELECT site_id, group_id, max(sent_date) AS sent_date
     FROM group_digest GROUP BY site_id,group_id) AS latest_digest, topic
  WHERE topic.site_id = latest_digest.site_id
    AND topic.group_id = latest_digest.group_id
    AND latest_digest.sent_date < CURRENT_TIMESTAMP-interval :interval
    AND topic.last_post_date > CURRENT_TIMESTAMP-interval :active_interval""")

        session = getSession()
        d = {'interval': interval, 'active_interval': active_interval}
        r = session.execute(s, params=d)
        retval = []
        if r.rowcount:
            retval = [{'site_id': x['site_id'],
                        'group_id': x['group_id']} for x in r]
        return retval

    def update_group_digest(self, site_id, group_id):
        """ Update the group_digest table when we send out a new digest.

        """
        dt = self.digestTable

        statement = dt.insert()

        session = getSession()
        session.execute(statement,
                        params={'site_id': site_id,
                                'group_id': group_id,
                                'sent_date': self.now})

        mark_changed(session)


class DigestQuery(TopicsQuery):

    def __init__(self):
        super(DigestQuery, self).__init__()

    def topics_sinse_yesterday(self, siteId, groupId):
        tt = self.topicTable
        tkt = self.topicKeywordsTable
        pt = self.postTable
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

        #SELECT topic.topic_id, topic.original_subject, topic.last_post_id,
        #  topic.last_post_date, topic.num_posts,
        cols = (tt.c.topic_id, tt.c.site_id, tt.c.group_id,
                tt.c.original_subject, tt.c.first_post_id,
                tt.c.last_post_id, tt.c.num_posts, tt.c.last_post_date,
                   tkt.c.keywords,
        #  (SELECT COUNT(*)
        #    FROM post
        #    WHERE (post.topic_id = topic.topic_id)
        #      AND post.date >= timestamp 'yesterday')
        #  AS num_posts_day
               sa.select([sa.func.count(pt.c.post_id)],
                         sa.and_(pt.c.date >= yesterday,
                         pt.c.topic_id == tt.c.topic_id)
                         ).as_scalar().label('num_posts_day'),
               sa.select([pt.c.user_id],
                         pt.c.post_id == tt.c.last_post_id
                         ).as_scalar().label('last_author_id'))
        s = sa.select(cols, order_by=sa.desc(tt.c.last_post_date))
        #  FROM topic
        #  WHERE topic.site_id = 'main'
        #    AND topic.group_id = 'mpls'
        s.append_whereclause(tt.c.site_id == siteId)
        s.append_whereclause(tt.c.group_id == groupId)
        #    AND topic.last_post_date >= timestamp 'yesterday'
        s.append_whereclause(tt.c.last_post_date >= yesterday)
        s.append_whereclause(tt.c.topic_id == tkt.c.topic_id)

        session = getSession()
        r = session.execute(s)

        retval = [{
                  'topic_id': x['topic_id'],
                  'subject': x['original_subject'],
                  'keywords': x['keywords'],
                  'first_post_id': x['first_post_id'],
                  'last_post_id': x['last_post_id'],
                  'last_post_date': x['last_post_date'],
                  'last_author_id': x['last_author_id'],
                  'num_posts': x['num_posts'],
                  'num_posts_day': x['num_posts_day'],
                  } for x in r]
        return retval
