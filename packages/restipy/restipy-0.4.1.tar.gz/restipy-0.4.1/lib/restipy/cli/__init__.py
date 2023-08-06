import argparse

from execute import do as execute
from store.list import do as store_list
from store.put import do as store_put
from store.get import do as store_get
from store.delete import do as store_delete
from store.clear import do as store_clear

from os.path import expanduser
home = expanduser("~")

parser = argparse.ArgumentParser()

parser.add_argument('--debug',
    dest='debug',
    action='store_true')

parser.add_argument('-v', '--verbose',
    dest='verbose',
    action='store_true')

parser.add_argument('--save-filename',
    dest='save_filename',
    default='{home}/.restipy/data.json'.format(home=home))

parser.add_argument('-e', '--env',
    dest='environment',
    default='default')

main_subparsers = parser.add_subparsers(help='Available commands.')


# Exec subparser

parser_exec = main_subparsers.add_parser('exec', help='Cookbook execution.')

parser_exec.add_argument('cookbook_file')

parser_exec.add_argument('-D', '--data',
    nargs='+',
    dest='data',
    default=[])

parser_exec.add_argument('-p', '--printer',
    help='''
        Defaut printer to use for output
        ''',
    # TODO: dynamically list printers
    choices=['silent', 'basic'],
    dest='printer_name',
    default='silent')

parser_exec.set_defaults(func=execute)


# Store subparser

parser_store = main_subparsers.add_parser('store', help='Manipulates the local store.')

store_subparsers = parser_store.add_subparsers(help='Commands to manipulate the local store')

parser_store_list = store_subparsers.add_parser('list', help='Prints the entire local store.')
parser_store_list.add_argument('-p', '--pretty',
    action='store_true')
parser_store_list.set_defaults(func=store_list)


parser_store_get = store_subparsers.add_parser('get', help='Gets a single item the local store.')
parser_store_get.add_argument('key')
parser_store_get.set_defaults(func=store_get)


parser_store_put = store_subparsers.add_parser('put', help='Put a single item in the local store.')
parser_store_put.add_argument('key')
parser_store_put.add_argument('value')
parser_store_put.set_defaults(func=store_put)

parser_store_delete = store_subparsers.add_parser('delete', help='Put a single item in the local store.')
parser_store_delete.add_argument('key')
parser_store_delete.set_defaults(func=store_delete)

parser_store_clear = store_subparsers.add_parser('clear', help='Clears the local store.')
parser_store_clear.set_defaults(func=store_clear)

args = parser.parse_args()
