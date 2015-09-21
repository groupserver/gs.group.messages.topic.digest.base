Changelog
=========

4.0.2 (2015-09-21)
------------------

* Using ``subject`` rather than ``Subject`` in ``mailto:`` URIs

4.0.1 (2015-05-04)
------------------

* Raising the correct error when a site is missing
* Added unit tests for the ``SendDigest.get_site`` and
  ``SendDigest.get_group`` methods

4.0.0 (2015-04-27)
------------------

* Splitting the web-hook in two:

  + Adding a page for getting a list of groups with a digest, and
  + Adding a page for sending a digest for a single group.

* Moving `the daily digest`_ to a new product
* Moving `the weekly digest`_ to a new product
* Removing the dynamic digest notifier, and making the digests
  themselves choose the notification that should go out.
* Added Sphinx documentation

.. _the daily digest:
   https://github.com/groupserver/gs.group.messages.topic.digest.daily

.. _the weekly digest:
   https://github.com/groupserver/gs.group.messages.topic.digest.weekly

3.0.0 (2015-03-03)
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
