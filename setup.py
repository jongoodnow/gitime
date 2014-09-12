#! /usr/bin/env python

import os
import sys
import codecs
from setuptools import setup
from setuptools.command.install import install as _install
import gitime.database as db

long_description = """
Keep track of your billable hours along with your commits. Gitime lets you build an invoice with your tasks and hours worked from your commit messages.

`Read the docs <http://gitime.readthedocs.org/en/latest/>`_ for more details

Simple Usage
------------

Set your hourly rate::

    $ gitime set -r 50

Start a new invoice::

    $ gitime invoice -n "Awesome Secret Project"

Time how long you've been working::

    $ gitime timer start

Make a commit as you would normally, but on the commit step, use :code:`gitime` instead of :code:`git`::

    $ git add feature.c
    $ gitime commit -m "Added a really cool thing"
    $ git push

Or, if you don't like timers, record the time yourself with the :code:`--hours` flag::

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

- `Git <http://git-scm.com/downloads>`_, and an executable called :code:`git` on your path
- `Python 2.7 <https://www.python.org/downloads/>`_ (or Python 3.4)

Install the latest release with::

    $ pip install gitime

Or install the development version with::

    $ git clone https://github.com/jongoodnow/gitime.git
    $ cd gitime
    $ pip install -r requirements.txt
    $ python setup.py install
"""


class install(_install):
    def run(self):
        _install.run(self)
        if not db.db_exists():
            DB_DIR = os.path.expanduser('~/.gitime')
            if not os.path.exists(DB_DIR):
                os.makedirs(DB_DIR)
                if os.name in ('posix', 'mac'):
                    db.set_unix_permissions(DB_DIR)
            db.first_time_setup()


setup(
    name="gitime",
    version="1.0.1",
    description="Build an invoice with your tasks and hours worked from your commit messages",
    long_description=long_description,
    author="Jonathan Goodnow",
    author_email="goodnow.jonathan@gmail.com",
    url="https://github.com/jongoodnow/gitime",
    keywords=['git', 'invoice', 'timer'],
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
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
    test_suite='tests',
    install_requires=['xlsxwriter']
)