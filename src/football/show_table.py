import re  # noqa: D100
from pathlib import Path

from numpy import reshape
from pandas import DataFrame, concat
from rich.console import Console
from rich.table import Table

from .format_tables import df_to_table, give_dataframe

console = Console()


def all_time_table(league: str, seasons: list):
    """Give DataFrame with all seasons."""
    cols = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    all_time_table = DataFrame(columns=cols)

    dfs = []
    marker = 50
    for season in seasons:
        # print(season)

        if int(season) > marker:
            df = give_dataframe(league, f"{season}", str(1900 + int(season) + 1)[-2:])
        else:
            df = give_dataframe(league, f"{season}", str(2000 + int(season) + 1)[-2:])

        df["Team"] = df["Team"].str.replace(r"\(.*\)", "", regex=True)
        df["Pts"] = df["Pts"].str.replace(r"\[.*\]", "", regex=True)
        df["Team"] = df["Team"].str.rstrip(" ")

        dfs.append(df)

    all_time_table = DataFrame(concat(dfs))

    columns = ["Pos", "Pts", "Pld", "W", "D", "L", "GF", "GA"]
    all_time_table[columns] = all_time_table[columns].astype(int)

    def _me_rule():
        return lambda row: sum(map(int, re.findall(r"(\d+|-\d+)", row)))

    all_time_table["GD"] = all_time_table["GD"].apply(_me_rule())

    new = all_time_table.groupby(by="Team", as_index=False).sum()
    df = DataFrame(new).sort_values("Pts", ascending=False).reset_index(drop=True)
    df.index = df.index + 1

    return df


def show_all_time_table(league: str, seasons: list):
    """Show all time table."""
    league_table = all_time_table(league, seasons)
    table = Table(title=league, header_style="bold magenta")
    console.print(df_to_table(league_table, table))
    # console.print(league_table)


def convert_data_to_df(league, season_start, season_end):
    """Convert txt data to dataframe."""
    folder = "data"
    path = f"{league}-{season_start}-{season_end}.txt"

    data = Path(Path(folder) / Path(path))
    data = list(data.read_text().splitlines())
    data = reshape(data, (int(len(data) / 10), 10))
    data = DataFrame(
        data, columns=["Team", "Pos", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    )

    return DataFrame(data)


def show_added_seasons(league: str):
    """Lazy way to show what we have in data."""
    print("showing seasons: ")
    files = list(Path("data/").glob("*.txt"))
    seasons = []
    for file in files:
        if league in str(file):
            seasons.append(file)

    for s in sorted(seasons):
        console.print(f"[bold cyan]{s}")


def read_results(team: str, league: str, season_start: str, season_end: str):
    """Gather results and place them on query."""
    import pandas as pd

    data = pd.read_csv(f"data/{league}_{season_start}_{season_end}_results.csv")
    home = data[data["Home"] == team]
    away = data[data["Away"] == team]
    table = Table(show_header=False, header_style="bold magenta")
    data = pd.concat([home, away])
    return df_to_table(data, table)
