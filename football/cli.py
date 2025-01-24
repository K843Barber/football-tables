"""CLI."""

import argparse
from typing import Callable, NamedTuple

from football.assets import other_logo
from football.common.clean_me import rinse
from football.common.config import configuration
from football.common.helper_functions import run_on_server
from football.get_table import get_alot, get_season, update_leagues
from football.prune import prune_leagues
from football.show_table import show_added_seasons, show_all_time_table, show_table
from football.tui.interactive import interactive as intermilan


class MyParser(argparse.ArgumentParser):
    """."""


class Option(NamedTuple):
    """."""

    function: Callable
    kwargs: dict


def main():
    """."""
    main_parser = MyParser(
        description=other_logo,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = main_parser.add_subparsers(dest="command")

    # --------------- Config ---------------
    subparsers.add_parser("config", help="Setup up leagues to get")
    # --------------- Get ---------------
    get = subparsers.add_parser("get", help="Get league standings")
    get.add_argument("league", help="Choose league", type=str)
    get.add_argument("season", nargs=2, help="Choose season")
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
    # --------------- prune ---------------
    subparsers.add_parser("prune", help="Remove any unwanted files")
    # --------------- update ---------------
    update = subparsers.add_parser("update", help="Update season")
    update.add_argument("--league", help="league")
    # --------------- clean ---------------
    clean = subparsers.add_parser("clean", help="Clean data, (dev)")
    clean.add_argument("league", help="Which league?)")

    args = {k.replace("-", "_"): v for k, v in vars(main_parser.parse_args()).items()}

    command = args.pop("command")

    subcommand = {
        "config": Option(configuration, {}),
        "get": Option(get_season, {**args}),
        "get_many": Option(get_alot, {**args}),
        "show": Option(show_table, {**args}),
        "interactive": Option(intermilan, {}),
        "show_seasons": Option(show_added_seasons, {**args}),
        "internet_me": Option(run_on_server, {}),
        "prune": Option(prune_leagues, {}),
        "all_time": Option(show_all_time_table, {**args}),
        "update": Option(update_leagues, {}),
        "clean": Option(rinse, {**args}),
        None: Option(main_parser.print_help, {}),
    }

    function, signature = subcommand[command]

    return function(**signature)


if __name__ == "__main__":
    raise SystemExit(main())
