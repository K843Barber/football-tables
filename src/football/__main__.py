#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

"""Add a configuration file, so we have some generics to store."""

import argparse
from json import load

import argcomplete
from argcomplete.completers import ChoicesCompleter

from .get_table import get_table
from .show_table import enrich_table, give_dataframe

with open(".config/configuration.json") as f:
    choices = tuple(load(f)['league'])

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers(dest='command')

# --------------- Get ---------------
get = subparsers.add_parser('get')
get.add_argument('--league',
                help='Choose league').completer = ChoicesCompleter(choices)
get.add_argument('--season',
                 nargs=2,
                 help='Choose season')
argcomplete.autocomplete(get)

# --------------- Show ---------------
show = subparsers.add_parser('show')
show.add_argument('--league',
                  help='Select league').completer = ChoicesCompleter(choices)
show.add_argument('--season',
                  nargs=2,
                  help='Select season')

argcomplete.autocomplete(show)
args = main_parser.parse_args()

def main():
    a1, a2, a3 = args.league, args.season[0], args.season[1]

    if args.command == "get":
        get_table(a1, a2, a3)
    elif args.command == "show":
        df = give_dataframe(a1,a2,a3)
        enrich_table(df, a1, a2, a3)

if __name__ == "__main__":
    main()
