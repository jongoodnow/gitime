Export
======

Export your invoice.

Usage
-----

::

	gitime export [-h] [-i [INVOICE]] [-f [FORMAT]] [-p [FILE]]

Options
-------

--invoice [INVOICE], -i [INVOICE]
*********************************

The name of the invoice to export. Defaults to your active invoice. See what invoice is active with :code:`gitime status`.

--format [FORMAT], -f [FORMAT]
******************************

Choose the export file format. This defaults to :code:`csv`. 

The formats currently available are:

- csv
- xlsx

--file [FILE], -p [FILE]
************************

The name of the file to write. Defaults to the name of the invoice with an appropriate extension.

--help, -h
**********

Display a help message.