#! /usr/bin/env python

import os
import sys
import codecs
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import gitime.database as db

long_description="""
======
gitime
======

Keep track of your billable hours along with your commits. Gitime lets you build an invoice with your tasks and hours worked from your commit messages.

`Read the docs <https://github.com/jongoodnow/gitime/tree/master/docs>`_ for more details

Simple Usage
------------

Set your hourly rate::

    $ gitime set -r 50

Start a new invoice::

    $ gitime invoice -n "Awesome Secret Project"

Time how long you've been working::

    $ gitime timer start

Make a commit as you would normally, but on the commit step, use `gitime` instead of `git`::

    $ git add feature.c
    $ gitime commit -m "Added a really cool thing"
    $ git push

Or, if you don't like timers, record the time yourself with the `--hours` flag::

    $ gitime commit -m "Proved Riemann Hypothesis" --hours 2

Look at your invoice::

    $ gitime status
    On invoice Awesome Secret Project
    Total time worked: 3 hours
    Total charges:     $150.00
    Charges:
    07-21-2014         1 hour          Added a really cool thing
    07-22-2014         2 hours         Proved Riemann Hypothesis

When it's time to bill, export your invoice to a spreadsheet. Currently, the only format available is csv. More formats are coming soon::

    $ gitime export

Installation
------------

You'll need two things installed to use gitime:

- `Git <http://git-scm.com/downloads>`_, and an executable called `git` on your path
- `Python 2.7 <https://www.python.org/downloads/>`_

Install the latest release with::

    $ pip install gitime --pre

Or install the development version with::

    $ git clone https://github.com/jongoodnow/gitime.git
    $ cd gitime
    $ python setup.py install

License
-------

`The MIT License <https://github.com/jongoodnow/gitime/blob/master/LICENSE>`_
"""

class install(_install):
    def run(self):
        _install.run(self)
        db.first_time_setup()

setup(
    name="gitime",
    version="1.3a",
    description="Build an invoice with your tasks and hours worked from your commit messages",
    long_description=long_description,
    author="Jonathan Goodnow",
    author_email="goodnow.jonathan@gmail.com",
    url="https://github.com/jongoodnow/gitime",
    keywords=['git', 'invoice', 'timer'],
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ],
    packages=['gitime'],
    entry_points={
        'console_scripts': [
            'gitime = gitime.cli:main'
        ]
    },
    cmdclass={
        'install': install
    },
    test_suite='tests'
)