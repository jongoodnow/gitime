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

The name of the invoice to export. Defaults to your active invoice. See what invoice is active with `gitime status`.

--format [FORMAT], -f [FORMAT]
******************************

Choose the format to export to. This defaults to `csv`. Right now, this is the only format available. More will come soon.

--file [FILE], -p [FILE]
************************

The name of the file to write. Defaults to the name of the invoice with an appropriate extension.

--help, -h
**********

Display a help message.