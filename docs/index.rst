Gitime
======

Gitime lets you keep track of your billable hours along with your commits. Build an invoice with your tasks and hours worked from your commit messages.

Installation
------------

Gitime can run on Linux, Windows, and Mac.

You'll only need two things installed to use gitime:

- `Git <http://git-scm.com/downloads>`_, and an executable called :code:`git` on your path
- `Python 2.7 <https://www.python.org/downloads/>`_ (or Python 3.4)

Install the latest gitime release with::

    $ pip install gitime

Or install the development version with::

    $ git clone https://github.com/jongoodnow/gitime
    $ cd gitime
    $ pip install -r requirements.txt
    $ python setup.py install

Getting Started
---------------

The first thing you should do is set your standard hourly rate, if you have one. You can manually set this for each invoice as well. To charge $50 per hour, run::

    $ gitime set -r 50

By default, gitime will round your hours worked to the nearest quarter hour. This can be changed to say, the nearest half-hour with::

    $ gitime set --round 0.5

Now, create your first invoice, named after whatever project you're working on. :code:`-r` and :code:`--round` are available here too, if you want a custom rate for this project::

    $ gitime invoice -n "Awesome Secret Project"

When you're ready to work, start the timer::

    $ gitime timer start

You can pause, reset, or check the timer by replacing :code:`start` with :code:`pause`, :code:`reset`, and :code:`status` respectively.

When you're ready, make your commit as you would normally, but change the :code:`git` to :code:`gitime` on the commit step::

    $ git add .
    $ gitime commit -m "Fixed a couple things"
    $ git push

Your time will be logged automatically, and the commit will be made. When you're ready for the next task, run :code:`gitime timer start` again and repeat the process.

If you don't want to use the timer and would rather keep track of the time yourself, run your commit with the :code:`--hours` flag::

    $ gitime commit -m "Fixed a couple things" --hours 3

If you don't want to actually want to make a commit but want to log a task, run the commit with the :code:`--fake` flag. Git will not be called.

You can check on your progress with::

    $ gitime status

Or export your invoice to csv or xlsx with::

    $ gitime export -f xlsx

Command Details
---------------

.. toctree::
    :maxdepth: 1
    
    invoices
    commits
    timer
    status
    export
    settings
    reset