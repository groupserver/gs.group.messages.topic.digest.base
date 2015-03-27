:mod:`gs.group.messages.topic.digest.base` API
==============================================

.. currentmodule:: gs.group.messages.topic.digest.base

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
