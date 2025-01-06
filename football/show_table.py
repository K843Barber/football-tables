"""Functions to show league tables."""

from pathlib import Path

from rich.console import Console

from football.common.all_time_helper import all_time_table
from football.common.format_tables import enrich_table, enrich_tablev4
from football.common.harry_styles import league_stylings
from football.common.helper_functions import convert_data_to_df, get_season_list

console = Console()


def show_all_time_table(league: str) -> None:
    """Show all time table."""
    seasons = get_season_list(league)
    league_table = all_time_table(league, seasons)
    title = str(league).replace("_", " ")
    console.print(enrich_tablev4(league_table, title), justify="center")


def show_added_seasons(league: str) -> None:
    """Lazy way to show what we have in data."""
    print("showing seasons: ")
    files = list(Path(f"data/{league}").glob("*.txt"))
    seasons = []
    for file in files:
        if league in str(file):
            seasons.append(file)

    for s in sorted(seasons):
        console.print(f"[bold cyan]{s}")


def show_table(league, season_start, season_end) -> None:
    """Show individual league table."""
    df = convert_data_to_df(league, season_start, season_end)
    styles = league_stylings[league][str(len(df))]
    title = str(league).replace("_", " ")
    enrich_table(df, title, season_start, season_end, styles)
