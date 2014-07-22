gitime
====

Keep track of your billable hours along with your commits. Gitime lets you build an invoice with your tasks and hours worked from your commit messages.

Simple Usage
----

Set your hourly rate.

	$ gitime settings -r 50

Start a new invoice.

	$ gitime invoice -n "Awesome Secret Project"

Time how long you've been working.

	$ gitime timer start

Make a commit as you would normally, but on the commit step, use `gitime` instead of `git`.

	$ git add amazingfeature.bf
	$ gitime commit -m "Added a really cool thing"
	$ git push

Look at your invoice.

	$ gitime status
	On invoice Awesome Secret Project
	Total time worked: 2 hours
	Total charges:     $100.00
	Charges:
	07-21-2014         2 hours         Added a really cool thing

When it's time to bill, export your invoice to a spreadsheet. Currently, the only format available is csv. More formats are coming soon.

	$ gitime export

Installation
----

You'll need two things installed to use gitime:

* [Git](http://git-scm.com/downloads)
* [Python 2.7](https://www.python.org/downloads/)

Install the latest release with:

	$ pip install gitime

Or install the development version with:

	$ git clone https://github.com/jongoodnow/gitime
	$ cd gitime
	$ python setup.py install

More information is available in the docs.