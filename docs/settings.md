Settings
====

Set up some default options.

Usage
----

	gitime set [-h] [--rate [RATE]] [--round [ROUND]] [--list]

Details
----

These options will change the defaults on invoices you create in the future. Existing invoices are not affected.

Options
----

####--rate [RATE], -r [RATE]

Set the hourly rate in dollars to be used by default on all future invoices.

####--round [ROUND]

Choose how to round hours worked. This defaults to the nearest quarter hour. For example, 2.71 hours will be rounded to 2.75 hours. If this setting is set to 0.5, 2.71 hours rounds to 2.5 hours.

####--list, -l

Display what the `--rate` and `--round` settings are currently set to.

####--help, -h

Display a help message.