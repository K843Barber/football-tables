"""CLI."""

import argparse
import sys

from football.assets import small_logo
from football.common import clean_me
from football.common.helper_functions import run_on_server
from football.get_table import get_alot, get_season, get_specific_season
from football.show_table import show_added_seasons, show_all_time_table, show_table
from football.tui.interactive import interactive as intermilan


class MyParser(argparse.ArgumentParser):
    """."""

    def error(self):
        """."""
        self.print_help()
        raise SystemExit("No Arguments Given")


def main():
    """."""
    main_parser = MyParser(
        description=small_logo,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = main_parser.add_subparsers(dest="command")

    # --------------- Get ---------------
    get = subparsers.add_parser("get", help="Get league standings")
    get.add_argument("league", help="Choose league", type=str)
    get.add_argument("season", nargs=2, help="Choose season")
    # --------------- Get Specific ---------------
    get_specific = subparsers.add_parser("get_specific", help="Get league standings")
    get_specific.add_argument("league", help="Choose league", type=str)
    get_specific.add_argument("season", nargs=2, help="Choose season")
    # --------------- Get_many ---------------
    get_many = subparsers.add_parser("get_many", help="Get multiple seasons")
    get_many.add_argument("league", help="Choose league", type=str)
    get_many.add_argument("season", nargs=2, help="Choose season")
    # --------------- Show ---------------
    show = subparsers.add_parser("show", help="Show a league table")
    show.add_argument("league", help="Select league")
    show.add_argument("season", nargs=2, help="Select season")
    # --------------- Show_all ---------------
    show_all = subparsers.add_parser("all_time", help="Show an all time league table")
    show_all.add_argument("league", help="Select league")
    # --------------- interactive ---------------
    subparsers.add_parser("interactive", help="Show in interactive mode")
    # --------------- show_seasons ---------------
    show_seasons = subparsers.add_parser("show_seasons", help="Show the saved seasons")
    show_seasons.add_argument("league", help="Which league seasons you currently have")
    # --------------- internet_it ---------------
    subparsers.add_parser("internet_me", help="Show table in browser")
    # --------------- clean_it ---------------
    clean = subparsers.add_parser("clean", help="Clean the data")
    clean.add_argument("league", help="league")
    # --------------- update ---------------
    update = subparsers.add_parser("update", help="Update season")
    update.add_argument("league", help="league")
    update.add_argument("season", nargs=2, help="Choose season")

    # args = main_parser.parse_args()
    args = main_parser.parse_args(None if sys.argv[1:] else ["--help"])

    if args.command == "get":
        get_season(args.league, *args.season)
    elif args.command == "get_many":
        get_alot(args.league, args.season[0], args.season[1])
    elif args.command == "get_specific":
        get_specific_season(args.league, *args.season)
    elif args.command == "show":
        show_table(args.league, *args.season)
    elif args.command == "interactive":
        intermilan()
    elif args.command == "show_seasons":
        show_added_seasons(args.league)
    elif args.command == "internet_me":
        run_on_server()
    elif args.command == "all_time":
        show_all_time_table(args.league)
    elif args.command == "clean":
        clean_me.clean_it(args.league)
        clean_me.clean_that(args.league)
    elif args.command == "update":
        get_season(args.league, *args.season)
        clean_me.clean_it(args.league)
        clean_me.clean_that(args.league)
    else:
        main_parser.print_help()


if __name__ == "__main__":
    main()
