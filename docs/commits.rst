.. commits:

Commits
=======

Run a regular git commit, but also log the commit message and time worked your active invoice.

Usage
-----

::

	gitime [-h] [--fake] [--hours [HOURS]] <your commit code ...>

Details
-------

Your commit must contain a message in the form :code:`-m [MSG]` or :code:`--message=[MSG]`

Options
-------

--fake
******

Your commit message and time will be logged in your active invoice, but no actual git commit will occur.

--hours [HOURS]
***************

In lieu of using the timer, you can manually specify the amount of hours worked. The number you enter is subject to the rounding rules set by your invoice. By default, this will round the number entered here to the nearest quarter hour. If the timer has not tracked any time, this option is required. Otherwise, the timer values are used by default if this option is not specified.

--help, -h
**********

Display a help message.