Changelog
=========

3.0.0 (2015-02-24)
------------------

* Renaming the product `gs.group.messages.topic.digest.base`_

.. _gs.group.messages.topic.digest.base:
   https://github.com/groupserver/gs.group.messages.topic.digest.base

2.3.2 (2014-06-04)
------------------

* Moving the SQL for creating the digest-related tables here.

2.3.1 (2014-02-20)
------------------

* Ensuring the headers are ASCII.

2.3.0 (2013-07-10)
------------------

* Using an adaptor to create the digest.
* Allowing sub-classes to overwrite the Message used in notifiers.
* Fixing permission problems.

2.2.0 (2013-06-24)
------------------

* Use a formatted-string rather than a date-object in the body of
  the daily-digest.
* Performance improvement.
* Raise a ``NoSuchListError`` rather than an ``AttributeError``.

2.1.0 (2013-03-12)
------------------

* Switch to a more flexible way to determine if a digest should be sent.
* Removed some logging.

2.0.1 (2013-02-19)
------------------

* Fixed ``sendQuery`` spelling.

2.0.0 (2012-12-22)
------------------

* First version that actually works.
* Use group-viewlets to construct the page.
* Moved all the digest-related code from external products here.


1.0.0 (2012-11-16)
------------------

* Initial version.

..  LocalWords:  Changelog
