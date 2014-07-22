gitime
====

Keep track of your billable hours along with your commits. Gitime lets you build an invoice with your tasks and hours worked from your commit messages.

[Read the docs](https://github.com/jongoodnow/gitime/tree/master/docs) for more details.

Simple Usage
----

Set your hourly rate.

	$ gitime set -r 50

Start a new invoice.

	$ gitime invoice -n "Awesome Secret Project"

Time how long you've been working.

	$ gitime timer start

Make a commit as you would normally, but on the commit step, use `gitime` instead of `git`.

	$ git add feature.c
	$ gitime commit -m "Added a really cool thing"
	$ git push

Or, if you don't like timers, record the time yourself with the `--hours` flag.

	$ gitime commit -m "Proved Riemann Hypothesis" --hours 2

Look at your invoice.

	$ gitime status
	On invoice Awesome Secret Project
	Total time worked: 3 hours
	Total charges:     $150.00
	Charges:
	07-21-2014         1 hour          Added a really cool thing
	07-22-2014         2 hours         Proved Riemann Hypothesis

When it's time to bill, export your invoice to a spreadsheet. Currently, the only format available is csv. More formats are coming soon.

	$ gitime export

Installation
----

You'll need two things installed to use gitime:

* [Git](http://git-scm.com/downloads), and an executable called `git` on your path
* [Python 2.7](https://www.python.org/downloads/)

Install the latest release with:

	$ pip install gitime --pre

Or install the development version with:

	$ git clone https://github.com/jongoodnow/gitime.git
	$ cd gitime
	$ python setup.py install

License
----

[The MIT License](https://github.com/jongoodnow/gitime/blob/master/LICENSE)