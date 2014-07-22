Status
====

See what commits are in your current invoice.

Usage
----

	gitime status [-h] [-i [INVOICE]]

Example
----

	$ gitime status
	Total Time Worked: 7.0 hours
	Total Charges:     $1400.00
	Charges:
	07-21-2014         2 hours         Fixed some css
	07-21-2014         1 hours         Added a functor
	07-21-2014         4 hours         Proved P!=NP

Options
----

####--invoice [INVOICE], -i [INVOICE]

Choose an invoice by name, instead of using the active one.

####--help, -h

Display a help message.