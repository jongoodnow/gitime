from __future__ import unicode_literals, print_function, division
import sys
import time
import math
import database as db

unix_now = lambda: math.floor(time.time())

class User(object):
    """ Contains user data that is shared between invoices """

    def __init__(self, rowid=1):
        meta = db.query_user(rowid)
        if not meta:
            print("User with rowid %s doesn't exist." %rowid, file=sys.stderr)
            sys.exit()
        self.rowid = rowid
        self.rate = meta[0]
        self.rounding = meta[1]
        self.timer_running = bool(meta[2])
        self.timer_start = meta[3]
        self.timer_total = meta[4]
        self.active_invoice_rowid = meta[5] if len(meta) == 6 else 0

    def _timer_db_update(self):
        """ Set the timer on the database to match 
            the timer of this object
        """
        db.update(lambda c: c.execute("""
            UPDATE user SET timer_running=?, timer_start=?, timer_total=?
            WHERE rowid=?
        """, (int(self.timer_running), self.timer_start, 
              self.timer_total, self.rowid
            )
        ))

    def start_timer(self):
        if self.timer_running:
            print("The timer is already running!", file=sys.stderr)
            sys.exit()
        self.timer_running = True
        self.timer_start = unix_now()
        self._timer_db_update()

    def reset_timer(self):
        self.timer_running = False
        self.timer_start = 0
        self.timer_total = 0
        self._timer_db_update()

    def pause_timer(self):
        if not self.timer_running:
            print("The timer isn't running.", file=sys.stderr)
            sys.exit()
        self.timer_running = False
        self.timer_total += unix_now() - self.timer_start
        self._timer_db_update()

    def time_tracked(self, inv=None):
        rounding = inv.rounding if inv else self.rounding
        if self.timer_running:
            return round((unix_now() - self.timer_start + self.timer_total) / 3600.0 / rounding) * rounding
        else:
            return round(self.timer_total / 3600.0 / rounding) * rounding

    def set_rate(self, r):
        self.rate = r
        db.update(lambda c: c.execute("""
            UPDATE user SET rate=? WHERE rowid=?
        """, (self.rate, self.rowid)))

    def set_rounding(self, r):
        self.rounding = r
        db.update(lambda c: c.execute("""
            UPDATE user SET rounding=? WHERE rowid=?
        """, (self.rounding, self.rowid)))

    def set_active_invoice(self, rowid):
        self.active_invoice_rowid = rowid
        db.update(lambda c: c.execute("""
            UPDATE user SET active_invoice=? WHERE rowid=?
        """, (self.active_invoice_rowid, self.rowid)))