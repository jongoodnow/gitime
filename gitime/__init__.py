from __future__ import unicode_literals, print_function
import sys
import textwrap


__title__ = 'gitime'
__version__ = '1.0.1'
__author__ = 'Jonathan Goodnow'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2014 Jonathan Goodnow'


def fprintf(*args, **kwargs):
    """ Output a string to the console, formatted to fit within 80 chars."""
    print(textwrap.fill(' '.join(args), 80), **kwargs)
