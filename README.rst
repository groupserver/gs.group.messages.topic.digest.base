=======================================
``gs.group.messages.topic.digest.base``
=======================================
~~~~~~~~~~~~~~~~~~~~
The digest of topics
~~~~~~~~~~~~~~~~~~~~

:Author: `Bill Bushey`_; `Michael JasonSmith`_
:Contact: Bill Bushey <wbushey@gmail.com>
:Date: 2015-04-27
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

The ``gs.group.messages.topic.digest.base`` product provides the
core infrastructure for creating and sending topic digests in a
GroupServer_ group. The notifier_ constructs the digests and
places them in an email message. The messages are normally
constructed from various `digest viewlets`_. This process is
coordinated by the `Digest groups`_ page and the `Send digest`_
page

Digest groups
=============

The *Digest groups* form,
``gs-group-messages-topic-digest-groups.html`` in the *site*
context, returns a list of groups that *can possibly* receive a
digest as a JSON object. It uses ``gs.auth.token`` [#token]_ for
authentication.

The list is calculated by looking up the groups that have a
member on digest mode (they have a ``digest`` entry in the
``setting`` column of the the ``email_setting`` table). The
returned JSON object is a list of site-identifiers and
group-identifiers that can be used with the `send digest`_ page.

Send digest
===========

A site wide form is available at
``gs-group-messages-topic-digest-send.html`` to initiate the
sending of a topics digest to a group. It uses ``gs.auth.token``
[#token]_ for authentication.

The form creates notifier_ for the group on the site, and calls
``notify()``.

Notifier
========

The notifier for a group creates some multiadaptors to create the
messages [#multiadaptor]_. It adapts the group and request to an
object that conforms to the
``gs.group.messages.topic.digest.base.interfaces.ITopicsDigestNotifier``. The
adaptors are sorted by their ``weight``, and the first one is
selected. The subject, plain-text message and HTML form of the
message is created from the adaptor, and then this is sent to all
group members that wish to receive the digest.

GroupServer_ ships with two digests by default:

* `Daily
  <https://github.com/groupserver/gs.group.messages.topic.digest.daily>`_
* `Weekly
  <https://github.com/groupserver/gs.group.messages.topic.digest.weekly>`_
 

Digest viewlets
===============

The
``gs.group.messages.topic.digest.base.viewlets.TopicsDigestViewlet``
is a ``gs.group.base.GroupViewlet`` that provides the
``topicsDigest`` property. This property is an instance of the
``gs.group.messages.topic.digest.base.topicdigest.BaseTopicsDigest``
class, that provides a list of topics to appear in the digest.

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.group.messages.topic.digest.base
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Bill Bushey: http://groupserver.org/p/wbushey
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#token] See <https://source.iopen.net/groupserver/gs.auth.token>

.. [#multiadaptor] See `Looking Up Adapters Using Multiple Objects
                   <http://docs.zope.org/zope.component/api/adapter.html#looking-up-adapters-using-multiple-objects>`_ 
                   for more on multiadaptors.

..  LocalWords:  multiadaptor multiadaptors Viewlets viewlets
