import argparse  # noqa: D100
from json import load

from rich import print

from football.__init__ import __version__
from football.football_app import FootballApp, run_on_server, ModesApp
from football.format_tables import enrich_table
from football.get_table import get_game_results, get_table
from football.show_table import (
    all_time_table,
    convert_data_to_df,
    give_dataframe,
    show_added_seasons,
    show_all_time_table,
)

with open(".config/configuration.json") as f:
    choices = tuple(load(f)["league"])

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers(dest="command")

# --------------- Get ---------------
get = subparsers.add_parser("get", help="Get archived or update current league standings")
get.add_argument("league", help="Choose league", type=str)
get.add_argument("season", nargs=2, help="Choose season")

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
interactive.add_argument("league", help="Choose league to include")
interactive.add_argument("season", nargs=2, help="Choose league to include")
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
tinternet.add_argument("league", help="Which league seasons you currently have")
tinternet.add_argument("season", nargs=2, help="From which season")


def main():
    """."""
    args = main_parser.parse_args()

    if args.command is None:
        print(f"[bold magenta]football version:[/bold magenta] {__version__}")
    else:
        try:
            league = args.league
            season_start = args.season[0]
            season_end = args.season[1]
        except Exception:  # noqa: BLE001
            league = args.league

        if args.command == "get":
            get_table(league, season_start, season_end)
        elif args.command == "show":
            df = give_dataframe(league, season_start, season_end)
            enrich_table(df, league, season_start, season_end)
        elif args.command == "interactive":
            ModesApp().run()

            # if int(season_end) - int(f"{season_start[:]}") == 1:
            #     df = convert_data_to_df(league, season_start, season_end[2:])
            #     FootballApp(df, league, season_start, season_end, False).run()
            # else:
            #     ss, se, ll = season_start, season_end, league
            #     df = all_time_table(ll, [str(i) for i in range(int(ss), int(se), 1)])
            #     FootballApp(df, league, season_start, season_end, True).run()

        elif args.command == "show_seasons":
            show_added_seasons(league)
        elif args.command == "get_game":
            get_game_results(league, season_start, season_end)
        elif args.command == "internet_me":
            run_on_server(league, season_start, season_end)
        else:
            show_all_time_table(
                league, [str(i) for i in range(int(season_start), int(season_end), 1)]
            )


if __name__ == "__main__":
    main()
