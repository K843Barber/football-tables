from pathlib import Path  # noqa: D100

from rich.console import Console
from rich.table import Table

from football.common.all_time_helper import all_time_table
from football.common.format_tables import df_to_table, enrich_table, give_dataframe

console = Console()


def show_all_time_table(league: str, start: str, end: str):
    """Show all time table."""
    seasons = [str(i) for i in range(int(start), int(end), 1)]
    league_table = all_time_table(league, seasons)
    table = Table(title=league, header_style="bold magenta")
    console.print(df_to_table(league_table, table), justify="center")


def show_added_seasons(league: str):
    """Lazy way to show what we have in data."""
    print("showing seasons: ")
    files = list(Path(f"data/{league}").glob("*.txt"))
    seasons = []
    for file in files:
        if league in str(file):
            seasons.append(file)

    for s in sorted(seasons):
        console.print(f"[bold cyan]{s}")


def show_table(league, season_start, season_end):
    """."""
    df = give_dataframe(league, season_start, season_end)
    enrich_table(df, league, season_start, season_end)
