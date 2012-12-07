Introduction
===========

gs.group.messages.topicsdigest provides the notifiers used to construct
topic digest emails and pages. This egg also provides a site level page - 
gs-group-messages-topicsdigest-send.html - that sends out digests for all
groups on the site.

Those interested in customizing the apperance of digests should pay attention
to Digest Body Viewlets and Headers and Footers.

- Code repository:
  https://source.iopen.net/groupserver/gs.group.messages.topicdigest
- Questions and comments to http://groupserver.org/groups/develop
- Report bugs at https://redmine.iopen.net/projects/groupserver


Types of Digests
===========

Three types of digests are available:
 
 * Daily Digest   - Digest of activity in a group from the previous 24 hours.
 * Weekly Digest  - Digest of activity for the seven most recently posted to
                    topics. Meant to be delivered as a weekly reminder to users.
 * Dynamic Digest - A daily digest if there has been activity in the group in
                    the previous 24 hours. Otherwise, a weekly digest.


Notifiers
===========

Three Notifiers are available in notifiers.py:

 * DailyTopicsDigestNotifier
 * WeeklyTopicsDigestNotifier
 * DynamicTopicsDigestNotifier

These classes provide a notify method, which sends digest emails to members of 
a group who are subscribed to digests. The body of these emails is construted 
using the Digest Pages described below (one for html emails, one for text 
emails) and the TopicsDigest objects described below. The email's  subject line
is also defined by the notifier classes using a TopicsDigest object.

Digest Pages
===========

The following pages are available for groups and produce full digest content:

 * Daily Digests
    gs-group-messages-topicsdigest-daily.html
    gs-group-messages-topicsdigest-daily.txt
  
 * Weekly Digests
    gs-group-messages-topicsdigest-weekly.html
    gs-group-messages-topicsdigest-weekly.txt

 * Dynamic Digests
    gs-group-messages-topicsdigest-dynamic.html
    gs-group-messages-topicsdigest-dynamic.txt

Classes for the above pages can be found in notifiermessages.py. Nothing very
interesting happens in the classes for Daily and Weekly digests. The classes for
Dynamic digests determine which of the other digests to render.

Templates for the above, dailyTopicsDigest-* and weeklyTopicsDigest-*, do
almost nothing of interest.


DailyTopicsDigest and WeeklyTopicsDigest
===========
DailyTopicsDigest and WeeklyTopicsDigest are data structures containing the 
information required for a daily or weekly topics digest. These classes, as 
well as their parent class BaseTopicsDigest, are defined in topicsDigest.py.

TopicsDigest classes provide two properties:

 * post_stats - A simple dict providing statistics about the topic digest
 * topics - A list containg dicts which provides info about each topic

See the docstrings for BaseTopicsDigest, DailyTopicsDigest, and 
WeeklyTopicsDigest for the attributes of the dicts provided by post_stats and 
topics.


Digest Viewlet Managers
===========

The following viewlet managers are used to add content to their respective 
rendered digest:

 * groupserver.DailyTopicsDigestHtmlVM
 * groupserver.DailyTopicsDigestTxtVM
 * groupserver.WeeklyTopicsDigestHtmlVM
 * groupserver.WeeklyTopicsDigestTxtVM

All use the same class - gs.viewlet.manager.WeightOrderedViewletManager - and 
the same template - topicsDigestVM.pt.

Digest Body Viewlets
===========

The following viewlets are used to create the body of topics digests:

 * groupserver.DailyTopicsDigestHtmlViewlet
 * groupserver.DailyTopicsDigestTxtViewlet
 * groupserver.WeeklyTopicsDigestHtmlViewlet
 * groupserver.WeeklyTopicsDigestTxtViewlet

Classes for these viewlets -TopicsDigestViewlet, DailyTopicsDigestViewlet, and
WeeklyTopicsDigestViewlet - can be found in viewlets.py. These classes primarily
decide which TopicsDigest class to use and provide the TopicsDigest.topics
property to templates when a digest page is called via the browser.

The design and layout of digest bodies are determinted by the templates for 
these viewlets: dailyTopicsDigestBody-* and weeklyTopicsDigestBody-*. 
These templates rely on the attributes provided by the dicts of 
TopicsDigest.topics to render the body of the topics digests.


Headers and Footers
===========

The following viewlets control the content, look, and design of the top portion
of digests:

 * groupserver.DailyTopicsDigestHeaderHtmlViewlet
 * groupserver.DailyTopicsDigestHeaderTxtViewlet
 * groupserver.WeeklyTopicsDigestHeaderHtmlViewlet
 * groupserver.WeeklyTopicsDigestHeaderTxtViewlet

The following viewlets control the content, look, and design of the bottom
portion of digests:

 * groupserver.DailyTopicsDigestFooterHtmlViewlet
 * groupserver.DailyTopicsDigestFooterTxtViewlet
 * groupserver.WeeklyTopicsDigestFooterHtmlViewlet
 * groupserver.WeeklyTopicsDigestFooterTxtViewlet

All of these viewlets rely on the HeaderFooterViewlet class, found in 
viewlets.py. The templates for these viewlets are header-* and footer-*.

Send All Digests
===========
A site wide form is available at gs-group-messages-topicsdigest-send.html to
initiate the sending of topics digests for all groups on the site. This form
uses gs.auth.token for authentication.

