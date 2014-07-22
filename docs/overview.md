Overview
====

Gitime lets you keep track of your billable hours along with your commits. Build an invoice with your tasks and hours worked from your commit messages.

Installation
----

Gitime is written in Python and has no dependencies outside of the Python standard library. This means that you can use it on a variety of platforms, such as Windows, Linux, or Mac.

You'll only need two things installed to use gitime:

* [Git](http://git-scm.com/downloads), and an executable called `git` on your path.
* [Python 2.7](https://www.python.org/downloads/)

Install the latest gitime release with:

	$ pip install gitime

Or install the development version with:

	$ git clone https://github.com/jongoodnow/gitime
	$ cd gitime
	$ python setup.py install

Getting Started
----

The first thing you should do is set your standard hourly rate, if you have one. You can manually set this for each invoice as well. To charge $50 per hour, run:

	$ gitime set -r 50

By default, gitime will round your hours worked to the nearest hour. This can be changed to say, the nearest half-hour with:

	$ gitime set --round 0.5

Now, create your first invoice, named after whatever project you're working on. `-r` and `--round` are available here too, if you want a custom rate for this project.

	$ gitime invoice -n "Awesome Secret Project"

When you're ready to work, start the timer.

	$ gitime timer start

You can pause, reset, or check the timer by replacing `start` with `pause`, `reset`, and `status` respectively.

When you're ready, make your commit as you would normally, but change the `git` to `gitime` on the commit step.

	git add .
	gitime commit -m "Fixed a couple things"
	git push

Your time will be logged automatically, and the commit will be made. When you're ready for the next task, run `gitime timer start` again and repeat the process.

If you don't want to use the timer and would rather keep track of the time yourself, run your commit with the `--hours` flag.

	gitime commit -m "Fixed a couple things" --hours 3

If you don't want to actually want to make a commit but want to log a task, run the commit with the `--fake` flag. Git will not be called.

You can check on your progress with `gitime status`, or export your invoice to csv with `gitime export`. More formats will be available soon.