:mod:`gs.group.messages.topic.digest.base` API
==============================================

.. currentmodule:: gs.group.messages.topic.digest.base

The main entry-point into the digest-code is the sender_ page,
which implements a *webhook* to send a digest to a single
group. The notifier_ sends out the message, which is constructed
by the message_ class.

Sender
------

.. autoclass:: gs.group.messages.topic.digest.base.sendDigests.SendDigest
   :members: get_site, get_group, get_digest_adapter

   .. method:: handle_send_all_digests(self, action, data)

      The form action for the *Send digest* page.

      :param action: The button that was clicked.
      :param dict data: The form data, containing the keys ``siteId`` and
         ``groupId``.

      The group (:meth:`.sendDigests.SendDigest.get_group`) is
      adapted to a digest
      (:meth:`.sendDigests.SendDigest.get_digest_adapter`). This
      digest is then sent to the group members using the notifier
      (:class:`.notifier.DigestNotifier`).

.. autoclass:: gs.group.messages.topic.digest.base.sendDigests.NoSuchSiteError
   :members:

.. autoclass:: gs.group.messages.topic.digest.base.sendDigests.NoSuchGroupError
   :members:

Notifier
--------

.. autoclass:: gs.group.messages.topic.digest.base.notifier.DigestNotifier
   :members: check_address, notify

   .. attribute:: digestMemberAddresses

      The list of email addresses of the group members that are
      configured to receive a digest.

.. autoclass:: gs.group.messages.topic.digest.base.notifier.NoSuchListError
   :members:

Message
-------

.. autoclass:: gs.group.messages.topic.digest.base.message.Message
   :members:
   :special-members: __str__
