import argparse  # noqa: D100

from football.common import clean_me
from football.common.helper_functions import run_on_server
from football.get_table import get_alot, get_game_results, get_table
from football.show_table import show_added_seasons, show_all_time_table, show_table
from football.tui.interactive import interactive as intermilan

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers(dest="command")

# --------------- Get ---------------
get = subparsers.add_parser("get", help="Get archived or update current league standings")
get.add_argument("league", help="Choose league", type=str)
get.add_argument("season", nargs=2, help="Choose season")
get_many = subparsers.add_parser("get_many", help="Get multiple seasons")
get_many.add_argument("league", help="Choose league", type=str)
get_many.add_argument("season", nargs=2, help="Choose season")

# --------------- Show ---------------
show = subparsers.add_parser("show", help="Show a particular league table")
show.add_argument("league", help="Select league")
show.add_argument("season", nargs=2, help="Select season")


# --------------- Show_all ---------------
show_all = subparsers.add_parser(
    "show_all", help="Show the all time league table of selected league"
)
show_all.add_argument("league", help="Select league")
show_all.add_argument("season", nargs=2, help="Select league")
# --------------- interactive ---------------
interactive = subparsers.add_parser("interactive", help="Show in interactive mode")
# --------------- show_seasons ---------------
show_seasons = subparsers.add_parser(
    "show_seasons", help="Show the seasons already added"
)
show_seasons.add_argument("league", help="Which league seasons you currently have")
# --------------- get_game_results ---------------
get_game = subparsers.add_parser("get_game", help="Get the results")
get_game.add_argument("league", help="From which league")
get_game.add_argument("season", nargs=2, help="From which season")
# --------------- internet_it ---------------
tinternet = subparsers.add_parser("internet_me", help="Show table in browser")
clean = subparsers.add_parser("clean", help="Clean the data")
clean.add_argument("league", help="league")


def main():
    """."""
    args = main_parser.parse_args()

    if args.command == "get":
        get_table(args.league, args.season[0], args.season[1])
    elif args.command == "get_many":
        get_alot(args.league, args.season[0], args.season[1])
    elif args.command == "show":
        show_table(args.league, args.season[0], args.season[1])
    elif args.command == "interactive":
        intermilan()
    elif args.command == "show_seasons":
        show_added_seasons(args.league)
    elif args.command == "get_game":
        get_game_results(args.league, args.season[0], args.season[1])
    elif args.command == "internet_me":
        run_on_server()
    elif args.command == "show_all":
        show_all_time_table(args.league, args.season[0], args.season[1])
    elif args.command == "clean":
        clean_me.clean_it(args.league)
        clean_me.clean_that(args.league)


if __name__ == "__main__":
    main()
