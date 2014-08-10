.. invoices:

Invoices
========

Switch to a different invoice, start a new one, or change invoice settings.

Usage
-----

::

	gitime invoice [-h] [-n] [--rate [RATE]] [--round [ROUND]] [--list] [name]

Details
-------

Invoices are used to store a log of your commit messages, commit dates, and hours worked.

Arguments
---------

name
****

The name of the invoice

Options
-------

--new, -n
*********

Create a new invoice, and make it the active invoice where future commits are sent. Without this option, if you give a :code:`name` that does not match any existing invoice, you will be asked if you want to make a new one.

--rate [RATE], -r [RATE]
************************

Set the hourly rate in dollars to be used on the invoice specified by :code:`name`.

--round [ROUND]
***************

Choose how to round hours worked on the invoice specified by :code:`name`. This defaults to the nearest hour. For example, 2.71 hours will be rounded to 3 hours. If this setting is set to 0.5, 2.71 hours rounds to 2.5 hours.

--list, -l
**********

Display a list of all your invoices.

--help, -h
**********

Display a help message.