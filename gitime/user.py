import sqlite3
from datetime import datetime
import calendar
import database as db

class User(object):
    """ Contains user data that is shared between invoices """

    def __init__(self, id=1):
        data = db.query('user', '*', {'rowid': 'id'}, True)
        self.rate = data[0]
        self.rounding = data[1]
        self.timer_running = bool(data[2])
        self.timer_start = data[3]
        self.timer_total = data[4]
        self.active_invoice = data[5]

    def start_timer(self):
        now = datetime.now()
        unix_now = calendar.timegm(d.tupletime())


def settings_main(args):
    print args

def status_main(args):
    print args

def timer_main(args):
    print args