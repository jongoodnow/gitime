#! /usr/bin/env python

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import gitime.database as db

class install(_install):
    def run(self):
        _install.run(self)
        db.first_time_setup()

setup(
    name="gitime",
    version="1.0a",
    description="build an invoice with your tasks and hours worked from your commit messages",
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