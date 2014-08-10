from __future__ import unicode_literals, print_function
from gitime.user import User
from gitime.commit import Commit, parse_hours_flag, parse_commit_message
from gitime.invoice import Invoice, InvoiceNotFound
import gitime.database as db
import sys
import textwrap
import os
import csv
import xlsxwriter
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
            Round hours to the nearest %g""" 
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
            try:
                inv = Invoice(args.name)
            except InvoiceNotFound:
                if raw_input("That invoice doesn't exist. Make a new one? [Y/n] ") == 'n':
                    sys.exit()
                inv = Invoice(args.name, new=True)
            if hasattr(args, 'rate'):
                inv.set_rate(args.rate)
            if hasattr(args, 'round'):
                inv.set_rounding(args.round)
            u = User()
            if u.active_invoice_rowid != inv.rowid:
                inv.set_active()
                print("Future commits will now be sent to the invoice %s." %inv.name)
    if args.list:
        u = User()
        count = db.invoice_count()
        noun = 'invoice' if count == 1 else 'invoices'
        print("You have %d %s:" %(count, noun))
        for invoice in db.query_all_invoices():
            if invoice[3] == u.active_invoice_rowid:
                active = " (active)"
            else:
                active = ""
            print(invoice[0], active)


def status_main(args):
    if hasattr(args, 'invoice'):
        inv = Invoice(args.invoice)
    else:
        u = User()
        invid = u.active_invoice_rowid
        if invid == 0:
            print("You do not have any invoices yet! Create one with `gitime invoice -n 'your invoice name'`.")
            sys.exit()
        inv = Invoice(u.active_invoice_rowid)
    total_hours = inv.total_hours()
    hourstr = 'hour' if total_hours == 1 else 'hours'
    print(textwrap.dedent("""\
        On invoice %s
        Total Time Worked: %g %s
        Total Charges:     $%.2f
        Charges:""" 
    %(inv.name, total_hours, hourstr, inv.total_earnings())))
    commits = inv.get_commit_meta()
    if not commits:
        print("No charges yet!")
    else:
        for com in commits:
            date = (datetime.fromtimestamp(com[1])).strftime('%m-%d-%Y')
            wspace1 = (17 - len(date)) * " "
            hourstr = 'hour' if com[2] == 1 else 'hours'
            hours = "%g %s" %(com[2], hourstr)
            wspace2 = (14 - len(hours)) * " "
            message = com[0]
            print(date, wspace1, hours, wspace2, message)


def timer_main(args):
    u = User()
    if not args.force:
        if u.active_invoice_rowid == 0:
            print(textwrap.fill((
                "WARNING: You do not have an active invoice set. "
                "You won't be able to record your hours without one. "
                "Create an invoice with the command: `gitime invoice -n <invoice name>` first, "
                "or suppress this warning by running the timer with the --force flag."), 
            80), file=sys.stderr)
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
        inv = Invoice(u.active_invoice_rowid)
        if u.timer_running:
            status = 'has been running since %s.' %str(datetime.fromtimestamp(u.timer_start))
        else:
            status = 'is not running.'
        print('The timer %s' %status)
        print('Total hours tracked: %.2f' %(u.time_tracked(inv)))


def commit_main(args):
    # commits are NOT handled by argparse. `args` are passed to this function
    # as they are from sys.argv.
    u = User()
    invid = u.active_invoice_rowid
    if invid == 0:
        print(textwrap.fill((
            "GITIME ERROR: You do not have an active invoice set. "
            "You won't be able to record your hours without one. "
            "Create an invoice with the command: `gitime invoice -n <invoice name>` first. "
            "Your commit has NOT been made."), 80), file=sys.stderr)
        sys.exit()
    inv = Invoice(invid)
    raw_hours = parse_hours_flag(args)
    if raw_hours is not False:
        hours = round(raw_hours / inv.rounding) * inv.rounding
    else:
        hours = u.time_tracked(inv)
        if hours <= 0:
            print(textwrap.fill((
                "GITIME ERROR: You didn't specify a number of hours, and the timer hasn't recorded anything. "
                "Run this command with the `--hours <hour count>` flag, or use the timer to track your time. "
                "Your commit has NOT been made."), 80), file=sys.stderr)
            sys.exit()
        u.reset_timer()
    message = parse_commit_message(args)
    if not message:
        print("GITIME ERROR: Could not find a message in your commit.", file=sys.stderr)
        sys.exit()
    com = Commit(message=message,
                 hours=hours,
                 invoice=u.active_invoice_rowid)
    print("GITIME: Your commit has been logged in invoice %s." %inv.name)
    if '--fake' not in args:
        print("GITIME: Running your commit now...")
        args[0] = 'git'
        os.system(" ".join(args))


def export_invoice_main(args):
    if hasattr(args, 'invoice'):
        try:
            inv = Invoice(args.invoice)
        except InvoiceNotFound:
            print("That invoice does not exist.", file=sys.stderr)
            sys.exit()
    else:
        u = User()
        if u.active_invoice_rowid == 0:
            print("You do not have an active invoice set. Create one with `gitime invoice -n <invoice name> first.",
                file=sys.stderr)
            sys.exit()
        inv = Invoice(u.active_invoice_rowid)
    if hasattr(args, 'file'):
        filename = args.file
    else:
        filename = inv.name
        commits = inv.get_commit_meta()
    if args.format == 'csv':
        if filename[-4:] != '.csv': 
            filename += '.csv'
        with open(filename, 'wb') as fi:
            writer = csv.writer(fi)
            writer.writerow(['Date', 'Hours', 'Task'])
            for com in commits:
                writer.writerow([(datetime.fromtimestamp(com[1])).strftime('%m-%d-%Y'), com[2], com[0]])
            writer.writerow([])
            writer.writerow(['Total Time Worked:', "%s" %inv.total_hours()])
            writer.writerow(['Total Charges:', "$%.2f" %inv.total_earnings()])
    elif args.format == 'xlsx':
        if filename[-4:] != '.xlsx': 
            filename += '.xlsx'
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 18)
        worksheet.set_column('C:C', 80)
        worksheet.write_string(0, 0, 'Date')
        worksheet.write_string(0, 1, 'Hours')
        worksheet.write_string(0, 2, 'Task')
        row = 1
        for com in commits:
            worksheet.write_string(row, 0, (datetime.fromtimestamp(com[1])).strftime('%m-%d-%Y'))
            worksheet.write_number(row, 1, com[2])
            worksheet.write_string(row, 2, com[0])
            row += 1
        row += 1
        worksheet.write_string(row, 0, 'Total Time Worked:')
        worksheet.write_number(row, 1, inv.total_hours())
        row += 1
        worksheet.write_string(row, 0, 'Total Charges:')
        worksheet.write_string(row, 1, '$%.2f' %inv.total_earnings())
        workbook.close()
    else:
        print("The format you specified is not supported at this time.",
            file=sys.stderr)


def reset_main(args):
    if not args.force:
        if raw_input(textwrap.fill((
            "WARNING: This will delete all invoices, commit logs, and user "
            "preferences. Your git repos won't be affected. You should export "
            "your invoices first. Are you sure? [y/N] "), 80)) not in ('y', 'Y'):
            sys.exit()
    db.first_time_setup()