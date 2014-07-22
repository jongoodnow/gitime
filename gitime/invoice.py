from __future__ import unicode_literals, print_function
import sys
import textwrap
from user import User
import database as db

class Invoice(object):

    def __init__(self, unique, new=False, rate=None, rounding=None, userid=1):
        """ Invoices can be instantiated from a rowid or a name.
            If the name isn't already in the database a new one
            will be created if `new` is true. Otherwise the program 
            halts. If instantiated from a rowid, using a rowid that 
            does not exist will throw an exception. `rate` and 
            `rounding` args unnecessary if querying by rowid. 
            `rate` and `rounding` default to user values.
        """
        self.user = User(userid)
        meta = db.query_invoice(unique)
        if meta:
            if new:
                print("An invoice with the name %s already exists. You can't make a new one with that name." %unique,
                    file=sys.stderr)
                sys.exit()
            self.name = meta[0]
            self.rate = meta[1]
            self.rounding = meta[2]
            self.rowid = meta[3] if len(meta) == 4 else unique
        else:
            # this will only happen if `unique` is a name
            # if `unique` is a rowid, an exception is raised
            # on the query.
            if not new:
                if raw_input("That invoice doesn't exist. Make a new one? [Y/n] ") == 'n':
                    sys.exit()
            self.name = unique
            if rate is None and self.user.rate == 0:
                print(textwrap.dedent("""\
                    WARNING: Your default hourly rate is set to zero. 
                    This means that no earnings will be recorded. 
                    You can set your default rate with `gitime set -r <rate>` or 
                    set the rate for this invoice with `gitime invoice <invoice name> -r <rate>`."""))
            self.rate = rate if rate is not None else self.user.rate
            self.rounding = rounding if rounding is not None else self.user.rounding
            self.rowid = db.insert_invoice(self.name, self.rate, self.rounding)

    def set_active(self):
        self.user.set_active_invoice(self.rowid)

    def set_rate(self, r):
        self.rate = r
        db.update(lambda c: c.execute("""
            UPDATE invoice SET rate=? WHERE rowid=?
        """, (self.rate, self.rowid)))

    def set_rounding(self, r):
        self.rounding = r
        db.update(lambda c: c.execute("""
            UPDATE invoice SET rounding=? WHERE rowid=?
        """, (self.rounding, self.rowid)))

    def get_commit_meta(self):
        return db.query_invoice_commit_meta(self.rowid)

    def total_hours(self):
        commits = self.get_commit_meta()
        return sum(commit[2] for commit in commits)

    def total_earnings(self):
        return self.total_hours() * self.rate