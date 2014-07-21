from __future__ import unicode_literals, print_function
import sys
import re
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
        self.date = date if date is not None else math.floor(time.time())
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


def parse_hours_flag(args):
    """ If the `--hours` flag was used, get the time, and remove 
        the flag and the time from the args list.
        Return FALSE if the flag was not present.
    """
    try:
        pos = args.index('--hours')
    except ValueError:
        return False
    else:
        hours = args[pos + 1]
        try:
            hours = float(hours)
        except ValueError:
            print("GITIME ERROR: %s is not a valid amount of hours. Your commit was NOT made. Try again." %hours,
                file=sys.stderr)
            sys.exit()
        else:
            del args[pos + 1]
            del args[pos]
            return hours


def parse_commit_message(args):
    """ Find the commit message in the commit command.
        Messages may be formatted like:
        * `-m "some message"`
        * `--message "some message"`
        * `--message="some message"`
        Single quotes are allowed too.
        `args` is a list that should be formatted exactly as sys.argv
    """
    reg = re.compile(r"(\-\w*m\w*|\-\-message)(\s*|(='(?:\\.|[^'])*'|\"(?:\\.|[^\"])*\"))")
    scan = [index for index, val in enumerate(args) for mat in [reg.search(val)] if mat]
    if not scan:
        return False
    if len(scan) > 1:
        print("GITIME ERROR: Your commit contains more than one message. Your commit was NOT made. Try again.",
            file=sys.stderr)
        sys.exit()
    index = scan[0]
    # check if the format is `--message="some message"`
    format_reg = re.search(r"='((\\.|[^'])*?)'|\"((\\.|[^\"])*?)\"", args[index])
    if format_reg is not None:
        return format_reg.group().strip('=').strip('"').strip("'")
    elif len(args) < index + 2:
        print("GITIME ERROR: Your commit doesn't contain a message. Your commit was NOT made. Try again.",
            file=sys.stderr)
        sys.exit()
    else:
        ret = args[index + 1]
        # add quotes to the message so that git can understand it when the command is run
        args[index + 1] = "".join(['"', args[index + 1], '"'])
        return ret