from __future__ import unicode_literals, division, absolute_import
from builtins import *  # noqa pylint: disable=unused-import, redefined-builtin

from argparse import ArgumentTypeError, ArgumentParser

from colorclass.toggles import disable_all_colors
from flexget import options
from flexget.event import event
from flexget.manager import Session
from flexget.plugins.filter.pending_approval import list_pending_entries, get_entry_by_id
from flexget.terminal import TerminalTable, TerminalTableError, table_parser, console, colorize
from sqlalchemy.orm.exc import NoResultFound


def valid_entry(value):
    try:
        int(value)
    except ValueError:
        if value != 'all':
            raise ArgumentTypeError('Must select \'all\' or valid entry ID')
    return value


def do_cli(manager, options):
    if hasattr(options, 'table_type') and options.table_type == 'porcelain':
        disable_all_colors()

    if options.action == 'list':
        list_entries(options)
    elif options.action == 'approve':
        manage_entries(options, options.selection, True)
    elif options.action == 'reject':
        manage_entries(options, options.selection, False)


def list_entries(options):
    """List pending entries"""
    approved = options.approved
    task_name = options.task_name

    with Session() as session:
        entries = list_pending_entries(session=session, task_name=task_name, approved=approved)
        header = ['#', 'Task Name', 'Title', 'URL', 'Approved', 'Added']
        table_data = [header]
        for entry in entries:
            table_data.append([
                entry.id,
                entry.task_name,
                entry.title,
                entry.url,
                colorize('green', 'Yes') if entry.approved else 'No',
                entry.added.strftime("%c"),
            ])
        table = TerminalTable(options.table_type, table_data, wrap_columns=[2, 1, 0], drop_columns=[4, 2])
        try:
            console(table.output)
        except TerminalTableError as e:
            console('ERROR: %s' % str(e))


def manage_entries(options, selection, approved):
    """Manage pending entries"""
    approved_text = 'approved' if approved else 'pending'
    with Session() as session:
        if selection == 'all':
            entries = list_pending_entries(session=session, approved=not approved)
        else:
            try:
                entry = get_entry_by_id(session, selection)
                if entry.approved is approved:
                    console(colorize('red', 'ERROR: ') + 'Entry with ID %s is already %s' % (entry.id, approved_text))
                    sys.exit(1)
            except NoResultFound:
                console('Pending entry with ID %s does not exist' % selection)
                sys.exit(1)
            else:
                entries = [entry]
        if not entries:
            console('All entries are already %s' % approved_text)
            return
        for entry in entries:
            if entry.approved is not approved:
                console('Setting pending entry with ID %s status to %s' % (entry.id, approved_text))
                entry.approved = approved


@event('options.register')
def register_parser_arguments():
    selection_parser = ArgumentParser(add_help=False)
    selection_parser.add_argument('selection', type=valid_entry,
                                  help='Entity ID or \'all\' to approve all pending entries')

    parser = options.register_command('pending', do_cli, help='View and pending')
    subparsers = parser.add_subparsers(title='actions', metavar='<action>', dest='action')

    list_parser = subparsers.add_parser('list', help='Shows all existing pending entries', parents=[table_parser])
    list_parser.add_argument('--task-name', help='Filter by task name')
    list_group = list_parser.add_mutually_exclusive_group()
    list_group.add_argument('--pending', action='store_false', help='Show only pending entries', dest='approved',
                            default=None)
    list_group.add_argument('--approved', action='store_true', help='Show only approved entries', dest='approved',
                            default=None)

    subparsers.add_parser('approve', help='Approve pending entries', parents=[selection_parser])
    subparsers.add_parser('reject', help='Reject pending entries', parents=[selection_parser])
