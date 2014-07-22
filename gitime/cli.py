from __future__ import unicode_literals
import argparse
import sys
import gitime
import commands


def add_subcommand(subparsers, name, help, func, args):
    subparser = subparsers.add_parser(name, help=help, description=help)
    for arg in args:
        subparser.add_argument(*arg[0], **arg[1])
    subparser.set_defaults(func=func)


def cmd_handler(cmd=None):
    parser = argparse.ArgumentParser(description='Keep track of your billable hours along with your commits.')
    parser.add_argument('-v', '--version', help='Show the version of gitime installed.', action='version', version="gitime %s" %gitime.__version__)

    subparsers = parser.add_subparsers()

    # include a commit subcommand for the help, even though it isn't used.
    add_subcommand(subparsers, 'commit', 'Run a regular git commit, but also log your time.', commands.commit_main, [])

    add_subcommand(subparsers, 'set', 'Set up some default options.', commands.settings_main, [
        ({'-r', '--rate',}, {
            'nargs': '?',
            'default': argparse.SUPPRESS,
            'help': 'Set the hourly rate that is used by default on all your invoices.',
        }),
        ({'--round',}, {
            'nargs': '?',
            'default': argparse.SUPPRESS,
            'help': 'Choose how to round the number of hours worked. Defaults to the nearest hour.',
        }),
        ({'-l', '--list',}, {
            'help': 'List the currently set rate and rounding',
            'action': 'store_true',
        }),
    ])

    add_subcommand(subparsers, 'invoice', 'Switch to a different invoice, start a new one, or change stats.', commands.invoice_main, [
        ({'name',}, {
            'help': 'The name of the invoice.',
            'nargs': '?',
            'default': argparse.SUPPRESS,
        }),
        ({'-n', '--new',}, {
            'help': 'Create a new invoice. Without this flag, switch to an invoice that already exists.',
            'action': 'store_true',
        }),
        ({'-r', '--rate',}, {
            'nargs': '?',
            'default': argparse.SUPPRESS,
            'help': 'Set the hourly rate. Defaults to the rate in your settings.',
        }),
        ({'--round',}, {
            'nargs': '?',
            'default': argparse.SUPPRESS,
            'help': 'Choose how to round the number of hours worked. Defaults to the nearest hour.',
        }),
        ({'-l', '--list',}, {
            'help': 'List all invoices.',
            'action': 'store_true',
        }),
    ])

    add_subcommand(subparsers, 'status', "See what's in your current invoice", commands.status_main, [
        ({'-i','--invoice'}, {
            'nargs': '?',
            'default': argparse.SUPPRESS,
            'help': 'Choose a different invoice to view the status of.',
        }),
    ])

    add_subcommand(subparsers, 'timer', 'Control your commit timer.', commands.timer_main, [
        ({'action',}, {
            'choices': ['start', 'pause', 'reset', 'status',],
            'help': 'Start the timer, pause it, or reset it. The timer is reset automatically when you make a commit.',
        }),
        ({'-f', '--force',}, {
            'help': 'Suppress warnings.',
            'action': 'store_true',
        }),
    ])

    add_subcommand(subparsers, 'export', 'Export an invoice.', commands.export_invoice_main, [
        ({'-i','--invoice'}, {
            'nargs': '?',
            'default': argparse.SUPPRESS,
            'help': 'The name of the invoice to export. Defaults to the active invoice',
        }),
        ({'-f', '--format',}, {
            'nargs': '?',
            'default': 'csv',
            'help': 'Choose the export format. Defaults to csv.',
        }),
        ({'-p', '--file',}, {
            'nargs': '?',
            'default': argparse.SUPPRESS,
            'help': 'The name of the file to write. Defaults to the name of the invoice with an appropriate extension.',
        }),
    ])

    add_subcommand(subparsers, 'reset', 'Deletes all invoices, commit records, and user preferences.', commands.reset_main, [
        ({'-f','--force'}, {
            'help': 'No confirmation message is sent before reset.',
            'action': 'store_true',
        }),
    ])

    if cmd:
        args = parser.parse_args(cmd)
    else:
        args = parser.parse_args()
        args.func(args)


def main():
    if len(sys.argv) == 1:
        cmd_handler(['-h'])
    elif sys.argv[1] == 'commit':
        # commits should not be handled by argparse because the command
        # string must remain intact
        if sys.argv[2] in ('-h', '--help'):
            # however, argparse makes a nice help screen, so we'll use
            # argparse here only if the user asks for help
            parser = argparse.ArgumentParser(description='Run a regular git commit, but also log your time.')
            parser.add_argument('--fake', help='Add this commit to the invoice, but don\'t make an actual commit.', action='store_true')
            parser.add_argument('--hours', help='Manually enter the time worked instead of using the timer.', nargs='?', default='argparse.SUPPRESS')
            args = parser.parse_args()
        else:
            commands.commit_main(sys.argv)
    else:
        # every other command gets handled by argparse
        cmd_handler()