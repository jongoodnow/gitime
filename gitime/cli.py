from __future__ import unicode_literals
import argparse
import commands


def add_subcommand(subparsers, name, help, func, args):
    subparser = subparsers.add_parser(name, help=help, description=help)
    for arg in args:
        subparser.add_argument(*arg[0], **arg[1])
    subparser.set_defaults(func=func)


def cmd():
    parser = argparse.ArgumentParser(description='Keep track of your billable hours along with your commits.')

    subparsers = parser.add_subparsers(help='sub-command help')

    add_subcommand(subparsers, 'commit', 'Run a regular git commit, but also log your time.', commands.commit_main, [
        ({'-a', '--all',}, {
            'action': 'store_true'
            'help': 'commit all changed files',
        }),
        ({'-q', '--quiet',}, {
            'action': 'store_true'
            'help': 'suppress summary after successful commit',
        }),
        ({'-v', '--verbose',}, {
            'action': 'store_true'
            'help': 'show diff in commit message template',
        }),
        ({'-s', '--signoff',}, {
            'action': 'store_true',
            'help': 'add Signed-off-by:',
        }),
        ({'--fake',}, {
            'action': 'store_true',
            'help': 'Add this commit to the invoice, but don\'t make an actual commit.',
        }),
        ({'-m', '--message',}, {
            'nargs': '?',
            'default': argparse.SUPPRESS,
            'help': 'commit message',
        }),
        ({'--time',}, {
            'nargs': '?',
            'default': argparse.SUPPRESS,
            'help': 'Manually enter the time worked instead of using the timer.',
        }),
    ])

    add_subcommand(subparsers, 'settings', 'Set up some default options.', commands.settings_main, [
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
            'default': 'CURRENT INVOICE',
            'help': 'The name of the invoice to export. Defaults to the active invoice',
        }),
        ({'-f', '--format',}, {
            'nargs': '?',
            'default': 'csv',
            'help': 'Choose the export format. Defaults to csv.',
        }),
    ])

    args = parser.parse_args()
    args.func(args)