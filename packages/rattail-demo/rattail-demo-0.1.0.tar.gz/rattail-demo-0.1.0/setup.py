# -*- coding: utf-8 -*-
"""
Setup script for Rattail Demo
"""

from __future__ import unicode_literals, absolute_import

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
execfile(os.path.join(here, 'rattail_demo', '_version.py'))
README = open(os.path.join(here, 'README.rst')).read()


requires = [
    #
    # Version numbers within comments below have specific meanings.
    # Basically the 'low' value is a "soft low," and 'high' a "soft high."
    # In other words:
    #
    # If either a 'low' or 'high' value exists, the primary point to be
    # made about the value is that it represents the most current (stable)
    # version available for the package (assuming typical public access
    # methods) whenever this project was started and/or documented.
    # Therefore:
    #
    # If a 'low' version is present, you should know that attempts to use
    # versions of the package significantly older than the 'low' version
    # may not yield happy results.  (A "hard" high limit may or may not be
    # indicated by a true version requirement.)
    #
    # Similarly, if a 'high' version is present, and especially if this
    # project has laid dormant for a while, you may need to refactor a bit
    # when attempting to support a more recent version of the package.  (A
    # "hard" low limit should be indicated by a true version requirement
    # when a 'high' version is present.)
    #
    # In any case, developers and other users are encouraged to play
    # outside the lines with regard to these soft limits.  If bugs are
    # encountered then they should be filed as such.
    #
    # package                           # low                   high

    'psycopg2',                         # 2.6.2
    'Tailbone',                         # 0.5.49
    'xlrd',                             # 1.0.0
]


setup(
    name = "rattail-demo",
    version = __version__,
    author = "Lance Edgar",
    author_email = "lance@edbob.org",
    url = "https://rattailproject.org/",
    description = "Rattail Software Demo",
    long_description = README,

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    install_requires = requires,
    packages = find_packages(),

    entry_points = {
        'paste.app_factory': [
            'main = rattail_demo.web.app:main',
        ],
    },
)
