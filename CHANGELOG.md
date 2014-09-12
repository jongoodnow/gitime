####1.0.1

* Linux and Mac DB permissions correctly set
* xlsxwriter now only required when exporting to xlsx
* Better exception handling
* Warns you if your database is missing

####1.0.0

* Support for Python 3.4
* Reinstalling the app no longer resets the database if it already exists
* Proper text overflow in console output
* `gitime export` will no longer ask you to create an invoice if you don't have any
* Documentation hosted on readthedocs.org
* `gitime commit` handles quotation marks in commit messages properly
* Support for Microsoft Excel (xlsx) exports
* Fixed RST inline code in docs
* `gitime invoice` now assumes the active invoice if no name is specified
* The `--round` flag can now be activated with `--rounding` or `-o`
* Flags in the help text now have consistant order

####1.3a

* fixed broken link in pypi long description
* fixed missing import for UNIX installs

####1.2a

* Corrected clone link in readme
* `gitime status` now says "hour" instead of "hours" when one hour is billed
* Windows and Mac now supported

####1.1a

* Switched pypi long description from markdown to restructured text

####1.0a

* The very first release