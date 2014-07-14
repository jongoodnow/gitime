from __future__ import unicode_literals, print_function
import sys
from user import User
import database as db

class Invoice(object):

	def __init__(self, unique, rate=None, rounding=None, userid=1):
		""" Invoice can be instantiated from a rowid or a name.
			If the name isn't already in the database a new one
			will be created. If instantiated from a rowid, using
			a rowid that does not exist will throw an exception.
			`rate` and `rounding` args unnecessary if querying by
			rowid. `rate` and `rounding` default to user values.
		"""
		meta = db.query_invoice(unique)
		if not meta:
			# this will only happen if `unique` is a name
			# if `unique` is a rowid, an exception is raised
			# on the query.
			self.name = unique
			user = User(userid)
			self.rate = rate if rate is not None else user.rate
			self.rounding = rounding if rounding is not None else user.rounding
			db.insert_invoice(self.name, self.rate, self.rounding)



