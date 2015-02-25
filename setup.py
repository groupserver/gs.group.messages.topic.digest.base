# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2013, 2014 E-Democracy.org and Contributors.
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
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()
name = 'gs.group.messages.topic.digest.base'

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(name=name,
      version=version,
      description="Provider of topic digest email notifiers",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "Intended Audience :: Developers",
          'License :: OSI Approved :: Zope Public License',
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='groupserver, email, digest, topic, notification',
      author='Bill Bushey',
      author_email='wbushey@acm.org',
      url='https://source.iopen.net/groupserver/{0}'.format(name),
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs', 'gs.group', 'gs.group.messages',
                          'gs.group.messages.topic',
                          'gs.group.messages.topic.digest'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pytz',
          'zope.browserpage',
          'zope.cachedescriptors',
          'zope.component',
          'zope.formlib',
          'zope.interface',
          'zope.tal',
          'zope.tales',
          'zope.viewlet',
          'Zope2',
          'gs.auth.token',
          'gs.content.form.base',
          'gs.core',
          'gs.email',
          'gs.group.base',
          'gs.viewlet',
          'Products.XWFCore',
          'Products.XWFMailingListManager',
      ],
      entry_points="""
          # -*- Entry points: -*-
      """,)
