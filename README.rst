==================================
``gs.group.messages.topicsdigest``
==================================
~~~~~~~~~~~~~~~~~~~~~~~~~~
The Daily Digest of Topics
~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Bill Bushey`_; `Michael JasonSmith`_
:Contact: Bill Bushey <wbushey@gmail.com>
:Date: 2013-07-10
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

The ``gs.group.messages.topicsdigest`` product provides the core
infrastructure for creating and sending topic digests in a group. Two types
of digests are sent:
 
#. Daily Digest — A summary of activity in a group from the previous 24
   hours.
#. Weekly Digest — A summary activity for the seven most recently posted to
   topics. This acts as a weekly reminder to the member that he or she is
   in the group.

The notifier_ constructs one of these two digests by creating the various
`digest pages`_ and placing them in an email message. This process is
triggered by the `Send All Digests`_ page

Notifier
========

The notifier for a group is a multiadaptor [#multiadaptor]_: it takes a
group, and a request, and returns an object that conforms to the
``gs.group.messages.topicsdigest.interfaces.ITopicsDigestNotifier``
interface. This object has a single ``notify`` method, which sends out the
notification to the group members who are configured to receive the daily
digest of topics.

The default adaptor provides a *dynamic* digest notifier, which selects
between the daily and weekly `digest pages`_, as needed:
``gs.group.messages.topicsdigest.notifiers.DynamicTopicsDigestNotifier``.
It passes the text and the HTML form of the digest to the
``gs.group.messages.topicsdigest.message.Message`` class to construct the
email-message. This message is then sent to the group members using
``gs.email.send_email`` [#send_email]_.

Specific group-types override the notifier by providing a different
adaptor. Closed groups, for example, provide a notifier that does nothing
when ``notify`` is called::

  <adapter
    for="gs.group.type.closed.interfaces.IGSClosedGroup
         zope.publisher.interfaces.browser.IBrowserRequest"
    provides="gs.group.messages.topicsdigest.interfaces.ITopicsDigestNotifier"
    factory="gs.group.type.closed.digest.ClosedGroupDigestNotifier" />


Digest Pages
============

There are **four** digest pages: a text and HTML version of the *daily* and
*weekly* digests. The following pages are produced in the context of a
group, and produce the full digest content:

+------------+-----------------------------------------------+------------------------------------------------+
|            | Text                                          | HTML                                           |
+============+===============================================+================================================+
| **Daily**  | ``gs-group-messages-topicsdigest-daily.txt``  | ``gs-group-messages-topicsdigest-daily.html``  |
+------------+-----------------------------------------------+------------------------------------------------+
| **Weekly** | ``gs-group-messages-topicsdigest-weekly.txt`` | ``gs-group-messages-topicsdigest-weekly.html`` |
+------------+-----------------------------------------------+------------------------------------------------+
  
Classes for the above pages can be found in
``gs.group.messages.topicsdigest.notifiermessages``. Nothing very
interesting happens in the classes for Daily and Weekly digests.

The templates for the above, ``dailyTopicsDigest-*`` and
``weeklyTopicsDigest-*``, do almost nothing of interest, as the content is
provided by the `Digest Viewlets`_.

The digests are abstracted into two classes:

#. ``gs.group.messages.topicsdigest.topicsDigest.DailyTopicsDigest``
#. ``gs.group.messages.topicsdigest.topicsDigest.WeeklyTopicsDigest``

They provide two properties:

:``post_stats``:
   A simple dictionary providing statistics about the topic digest.

:``topics``:
   A list containing dictionaries that provide information about each
   topic.

Digest Viewlets
===============

The viewlets for the digests follow the same four-way split — between text
and html, and daily and weekly — as is seen in the `digest pages`_. Four
`viewlet managers`_ provide space for the `body viewlets`_, the headers_
and footers_.

Viewlet Managers
----------------

The following viewlet managers are used to add content to their respective
rendered digest:

+------------+-----------------------------------------+------------------------------------------+
|            | Text                                    | HTML                                     |
+============+=========================================+==========================================+
| **Daily**  | ``groupserver.DailyTopicsDigestTxtVM``  | ``groupserver.DailyTopicsDigestHtmlVM``  |
+------------+-----------------------------------------+------------------------------------------+
| Interface  | ``IDailyTopicsDigestTxtVM``             | ``IDailyTopicsDigestHtmlVM``             |
+------------+-----------------------------------------+------------------------------------------+
| **Weekly** | ``groupserver.WeeklyTopicsDigestTxtVM`` | ``groupserver.WeeklyTopicsDigestHtmlVM`` |
+------------+-----------------------------------------+------------------------------------------+
| Interface  | ``IWeeklyTopicsDigestTxtVM``            | ``IWeeklyTopicsDigestHtmlVM``            |
+------------+-----------------------------------------+------------------------------------------+

All differ in name only: they use the same class —
``gs.viewlet.manager.WeightOrderedViewletManager`` — and the same template
— ``topicsDigestVM.pt``.

Body Viewlets
-------------

The following viewlets are used to create the body of topics digests:

+------------+----------------------------------------------+-----------------------------------------------+
|            | Text                                         | HTML                                          |
+============+==============================================+===============================================+
| **Daily**  | ``groupserver.DailyTopicsDigestTxtViewlet``  | ``groupserver.DailyTopicsDigestHtmlViewlet``  |
+------------+----------------------------------------------+-----------------------------------------------+
| Class      | ``gs.group.messages.topicsdigest.viewlets.DailyTopicsDigestViewlet``                         |
+------------+----------------------------------------------+-----------------------------------------------+
| **Weekly** | ``groupserver.WeeklyTopicsDigestTxtViewlet`` | ``groupserver.WeeklyTopicsDigestHtmlViewlet`` |
+------------+----------------------------------------------+-----------------------------------------------+
| Class      | ``gs.group.messages.topicsdigest.viewlets.WeeklyTopicsDigestViewlet``                        |
+------------+----------------------------------------------+-----------------------------------------------+

The design and layout of digest bodies are determinted by the templates for
these viewlets: ``dailyTopicsDigestBody-*`` and
``weeklyTopicsDigestBody-*``. These templates rely on the attributes
provided by the dictionaries of ``TopicsDigest.topics`` to render the body
of the topics digests.

Headers
-------

The following viewlets control the content, look, and design of the top
portion of digests:

+------------+----------------------------------------------------+-----------------------------------------------------+
|            | Text                                               | HTML                                                |
+============+====================================================+=====================================================+
| **Daily**  | ``groupserver.DailyTopicsDigestHeaderTxtViewlet``  | ``groupserver.DailyTopicsDigestHeaderHtmlViewlet``  |
+------------+----------------------------------------------------+-----------------------------------------------------+
| **Weekly** | ``groupserver.WeeklyTopicsDigestHeaderTxtViewlet`` | ``groupserver.WeeklyTopicsDigestHeaderHtmlViewlet`` |
+------------+----------------------------------------------------+-----------------------------------------------------+

Footers
-------

The following viewlets control the content, look, and design of the bottom
portion of digests:

+------------+----------------------------------------------------+-----------------------------------------------------+
|            | Text                                               | HTML                                                |
+============+====================================================+=====================================================+
| **Daily**  | ``groupserver.DailyTopicsDigestFooterTxtViewlet``  | ``groupserver.DailyTopicsDigestFooterHtmlViewlet``  |
+------------+----------------------------------------------------+-----------------------------------------------------+
| **Weekly** | ``groupserver.WeeklyTopicsDigestFooterTxtViewlet`` | ``groupserver.WeeklyTopicsDigestFooterHtmlViewlet`` |
+------------+----------------------------------------------------+-----------------------------------------------------+

Send All Digests
================

A site wide form is available at
``gs-group-messages-topicsdigest-send.html`` to initiate the sending of
topics digests for all the groups. It uses ``gs.auth.token`` [#token]_ for
authentication.

When submitted the form iterates through each of the sites on the
GroupServer instance, creating a digest notifier_ for each group on the
site, and calling ``notify()``.

Resources
=========

- Code repository:
  https://source.iopen.net/groupserver/gs.group.messages.topicsdigest
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Bill Bushey: http://groupserver.org/p/wbushey
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#multiadaptor] See `Looking Up Adapters Using Multiple Objects
                   <http://docs.zope.org/zope.component/api/adapter.html#looking-up-adapters-using-multiple-objects>`_ 
                   for more on multiadaptors.
.. [#send_email] See <https://source.iopen.net/groupserver/gs.email>

.. [#token] See <https://source.iopen.net/groupserver/gs.auth.token>
