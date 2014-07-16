from __future__ import unicode_literals
import sys
import math
import time
from user import User
from invoice import Invoice
import database as db

class Commit(object):

    def __init__(self, message, hours, invoice, date=None, rowid=None, new=True):
        """ creates a new commit and adds it to the database. To access
            an existing commit, do not access this constructor directly.
            Instead, use the `access` class method.
            Args:
            * message - the commit message
            * hours - the hours worked
            * invoice - the invoice rowid, or name
            * date - unix date of commit. Use None to determine the date
                     automatically
            * rowid - this is provided by the `access` method
            * new - create a new commit. If false, access an existing one
        """
        self.message = message
        self.hours = hours
        self.invoice = Invoice(invoice)
        if date:
            self.date = date
        else:
            self.date = math.floor(time.time())
        if new:
            self.rowid = db.insert_commit(
                self.message, self.date, self.hours, self.invoice.rowid)
        elif rowid:
            self.rowid = rowid
        else:
            raise Exception("Rowid must be provided to access an existing commit")

    @classmethod
    def access(cls, rowid):
        commit = db.query_commit(rowid)
        return cls(commit[0], commit[2], commit[3], commit[1], rowid, False)