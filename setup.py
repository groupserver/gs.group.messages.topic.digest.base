# coding=utf-8
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.group.messages.topicsdigest',
    version=version,
    description="Provider of topic digest email notifiers",
    long_description=open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
      "Development Status :: 2 - Alpha",
      "Environment :: Web Environment",
      "Framework :: Zope2",
      "Intended Audience :: Developers",
      "License :: Other/Proprietary License",
      "Natural Language :: English",
      "Operating System :: POSIX :: Linux"
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='groupserver email digest',
    author='Bill Bushey',
    author_email='wbushey@acm.org',
    url='http://www.groupserver.org/',
    license='other',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.group', 'gs.group.messages'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
        'pytz',
        'zope.cachedescriptors',
        'zope.component',
        'zope.formlib',
        'zope.interface',
        'zope.viewlet',
        'Zope2',
        'gs.auth.token',
        'gs.content.form',
        'gs.email',
        'gs.group.base >= 2.0',
        'gs.viewlet',
        'Products.XWFCore',
        'Products.XWFMailingListManager',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)
