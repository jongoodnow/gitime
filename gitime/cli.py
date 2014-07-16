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
        ({'args',}, {
            'nargs': '+',
            'help': 'The normal arguments you would pass to your git commit.',
        }),
    ])

    add_subcommand(subparsers, 'settings', 'Set up some default options.', commands.settings_main, [
        ({'-r', '--rate',}, {
            'nargs': '?',
            'default': '0',
            'help': 'Set the hourly rate that is used by default on all your invoices.',
        }),
        ({'--round',}, {
            'nargs': '?',
            'default': '1',
            'help': 'Choose how to round the number of hours worked. Defaults to the nearest hour.',
        }),
    ])

    add_subcommand(subparsers, 'new-invoice', 'Start a new invoice.', commands.new_invoice_main, [
        ({'name',}, {
            'help': 'The name of the new invoice.',
        }),
        ({'-r', '--rate',}, {
            'nargs': '?',
            'default': '10',
            'help': 'Set the hourly rate. Defaults to the rate in your settings.',
        }),
        ({'--round',}, {
            'nargs': '?',
            'default': '1',
            'help': 'Choose how to round the number of hours worked. Defaults to the nearest hour.',
        }),
    ])

    add_subcommand(subparsers, 'checkout-invoice', 'Switch your new commits to a different invoice.', commands.checkout_invoice_main, [
        ({'name',}, {
            'help': 'Name of invoice to checkout.',
        }),
    ])

    add_subcommand(subparsers, 'status', "See what's in your current invoice", commands.status_main, [
        ({'-i','--invoice'}, {
            'nargs': '?',
            'default': 'CURRENT INVOICE',
            'help': 'Choose a different invoice to view the status of.',
        }),
    ])

    add_subcommand(subparsers, 'timer', 'Control your commit timer.', commands.timer_main, [
        ({'action',}, {
            'choices': ['start', 'pause', 'reset',],
            'help': 'Start the timer, pause it, or reset it. The timer is reset automatically when you make a commit.',
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