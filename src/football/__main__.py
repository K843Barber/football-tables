#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

"""Add a configuration file, so we have some generics to store."""

import argparse
from json import load

import argcomplete
from argcomplete.completers import ChoicesCompleter

from .get_table import get_table
from .show_table import all_time_table, enrich_table, give_dataframe

with open(".config/configuration.json") as f:
    choices = tuple(load(f)["league"])

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers(dest="command")

# --------------- Get ---------------
get = subparsers.add_parser("get", help="Get archived or update current league standings")
get.add_argument("--league", help="Choose league").completer = ChoicesCompleter(choices)
get.add_argument("--season", nargs=2, help="Choose season")
argcomplete.autocomplete(get)

# --------------- Show ---------------
show = subparsers.add_parser("show", help="Show a particular league table")
show.add_argument("--league", help="Select league").completer = ChoicesCompleter(choices)
show.add_argument("--season", nargs=2, help="Select season")

argcomplete.autocomplete(show)

show_all = subparsers.add_parser("show_all", help="Show the all time league table of selected league")
show_all.add_argument("--league", help="Select league").completer = ChoicesCompleter(choices)
args = main_parser.parse_args()


def main():
    try:
        a1, a2, a3 = args.league, *args.season
    except ValueError("Continue"):
        # ValueError("Continue")
        a1 = args.league

    if args.command == "get":
        get_table(a1, a2, a3)
    elif args.command == "show":
        df = give_dataframe(a1, a2, a3)
        enrich_table(df, a1, a2, a3)
    else:
        all_time_table(a1, [str(i)[-2:] for i in range(1992, 2025, 1)])


if __name__ == "__main__":
    main()
