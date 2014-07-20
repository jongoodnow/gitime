from __future__ import unicode_literals, print_function
from user import User
from commit import Commit, parse_hours_flag, parse_commit_message
from invoice import Invoice
import database as db
import sys
import textwrap
import os
from datetime import datetime

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
            Hourly Rate: $%.2f
            Round to: %f""" 
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
            inv.set_active()
            print("Future commits will now be sent to the invoice %s." %inv.name)
        else:
            inv = Invoice(args.name)
            if hasattr(args, 'rate'):
                inv.set_rate(args.rate)
            if hasattr(args, 'round'):
                inv.set_rounding(args.round)
            u = User()
            if u.active_invoice_rowid != inv.rowid:
                inv.set_active()
                print("Future commits will now be sent to the invoice %s." %inv.name)
    if args.list:
        count = db.invoice_count()[0]
        noun = 'invoice' if count == 1 else 'invoices'
        print("You have %d %s:" %(count, noun))
        for invoice in db.query_all_invoices():
            print(invoice[0])


def status_main(args):
    if hasattr(args, 'invoice'):
        inv = Invoice(args.invoice)
    else:
        u = User()
        inv = Invoice(u.active_invoice_rowid)
    print(textwrap.dedent("""\
        On invoice %s
        Total Time Worked: %s hours
        Total Charges:     $%.2f
        Charges:""" 
    %(inv.name, inv.total_hours(), inv.total_earnings())))
    commits = inv.get_commits()
    for com in commits:
        hours = "%r hours" %com[2]
        wspace = 19 - len(hours) * " "
        message = com[1]
        print(hours, wspace, message)


def timer_main(args):
    u = User()
    if not args.force:
        if u.active_invoice_rowid == 0:
            print(textwrap.dedent("""\
                WARNING: You do not have an active invoice set. 
                You won't be able to record your hours without one.
                Create an invoice with the command: `gitime invoice -n <invoice name>` first,
                or suppress this warning by running the timer with the --force flag."""), file=sys.stderr)
            sys.exit()
    if args.action == 'start':
        u.start_timer()
        print('Timer started at %s' %str(datetime.now()))
    elif args.action == 'pause':
        u.pause_timer()
        print('Timer paused at %s' %str(datetime.now()))
    elif args.action == 'reset':
        u.reset_timer()
    elif args.action == 'status':
        if u.timer_running:
            status = 'has been running since %s.' %str(datetime.fromtimestamp(u.timer_start))
        else:
            status = 'is not running.'
        print('The timer %s' %status)
        print('Total hours tracked: %.2f' %(u.time_tracked() / 3600))


def commit_main(args):
    # commits are NOT handled by argparse `args` are passed to this function
    # as they are from sys.argv.
    u = User()
    inv = Invoice(u.active_invoice_rowid)
    if u.active_invoice_rowid == 0:
        print(textwrap.dedent("""\
            GITIME ERROR: You do not have an active invoice set. 
            You won't be able to record your hours without one.
            Create an invoice with the command: `gitime invoice -n <invoice name>` first.
            Your commit has NOT been made."""), file=sys.stderr)
        sys.exit()
    hours = parse_hours_flag(args)
    if not hours:
        hours = u.time_tracked()
        if u.time_tracked() <= 0:
            print(textwrap.dedent("""\
                GITIME ERROR: You didn't specify a number of hours, and the timer hasn't recorded anything.
                Run this command with the `--hours <hour count>` flag, or use the timer to track your time.
                Your commit has NOT been made."""), file=sys.stderr)
            sys.exit()
        u.reset_timer()
    com = Commit(message=parse_commit_message(args),
                 hours=hours,
                 invoice=u.active_invoice_rowid)
    print("GITIME: Your commit has been logged in invoice %s." %inv.name))
    if '--fake' not in args:
        print("GITIME: Running your commit now...")
        os.system(" ".join(args))


def export_invoice_main(args):
    pass