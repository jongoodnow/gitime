from __future__ import unicode_literals, print_function
from user import User
from commit import Commit
from invoice import Invoice
import database as db
import sys
import textwrap

def settings_main(args):
    u = User()
    if hasattr(args, 'rate'):
        u.set_rate(args.rate)
        print("The rate of $%s per hour will be applied to all new invoices." %args.rate)
    if hasattr(args, 'round'):
        u.set_rounding(args.round)
        print("Hours will be rounded to the nearest %s on all new invoices" %args.round)
    if args.list:
        print(textwrap.dedent("""\
            These are your default values for all invoices created in the future:
            Hourly Rate: %s
            Round to: %s""" 
        %(u.rate, u.rounding)))


def invoice_main(args):
    if hasattr(args, 'name'):
        if args.new:
            kwargs = {'new': True}
            if hasattr(args, 'rate'):
                kwargs['rate'] = args.rate
            if hasattr(args, 'round'):
                kwargs['rounding'] = args.round
            inv = Invoice(args.name, **kwargs)
        else:
            inv = Invoice(args.name)
            if hasattr(args, 'rate'):
                inv.set_rate(args.rate)
            if hasattr(args, 'round'):
                inv.set_rounding(args.round)
        inv.set_active()
        print("Future commits will now be sent to the invoice %s." %inv.name)
    if args.list:
        count = db.invoice_count()[0]
        noun = 'invoice' if count == 1 else 'invoices'
        print("You have %d %s:" %(count, noun))
        for invoice in db.query_all_invoices():
            print(invoice[0])


def status_main(args):
    pass


def timer_main(args):
    pass


def commit_main(args):
    pass


def export_invoice_main(args):
    pass