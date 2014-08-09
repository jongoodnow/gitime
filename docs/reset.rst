Reset
=====

Delete all your records and start afresh.

Usage
-----

::

	gitime reset [-h] [--force]

Details
-------

This command will do the following:

- Erase all commit records on invoices (your actual git repo won't be affected)
- Erase all invoices
- Reset all default settings

Basically, gitime will be as it was when you first installed it.

**This cannot be undone.** You should export your invoices first.

Options
-------

--force, -f
***********

This option is for the bold. Without it, you will be asked if you are sure you want to do this first. With it, no checks will occur.

--help, -h
**********

Display a help message.