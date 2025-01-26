"""Helper functions for all time table."""

from pathlib import Path

from pandas import DataFrame, concat
from rich.table import Table

from football.common.format_tables import df_to_table
from football.common.helper_functions import convert_data_to_df
from football.common.league_page_helper import read_seasons


def all_time_table(league: str, seasons: list) -> DataFrame:
    """Give DataFrame with all seasons."""
    cols = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    all_time = DataFrame(columns=cols)

    dfs = []
    for season in seasons:
        dfs.append(convert_data_to_df(league, f"{season}", f"{int(season) + 1}"))

    all_time = DataFrame(concat(dfs))
    columns = ["Pos", "Pts", "Pld", "W", "D", "L", "GF", "GA"]
    all_time[columns] = all_time[columns].astype(int)
    all_time["GD"] = all_time["GD"].str.replace("−", "-")  # noqa: RUF001
    all_time["GD"] = all_time["GD"].astype(int)

    new = all_time.groupby(by="Team", as_index=False).sum()
    df = DataFrame(new).sort_values("Pts", ascending=False).reset_index(drop=True)
    df["Pos"] = df.index + 1
    df[["Team", "Pos"]] = df[["Pos", "Team"]]
    return df


def get_smallest(league: str) -> int:
    """Grab the earliest season for the all time table."""
    return min([int(i.split("_")[0]) for i in read_seasons(league)])


def league_winners(league: str) -> Table:
    """."""
    path = Path.cwd() / "data/leagues" / league
    files = path.rglob("*.txt")

    titles: dict = {}

    for file in sorted(files)[:-1]:
        winner = file.read_text().split("\n")[0]
        if winner in titles:
            titles[winner] += 1
        else:
            titles[winner] = 1

    titles = dict(sorted(titles.items(), key=lambda item: item[1], reverse=True))
    titles_df = DataFrame(titles, index=["0"]).T
    titles_df["Team"] = titles_df.index
    titles_df.columns = ["Wins", "Team"]
    titles_df = titles_df[["Team", "Wins"]]
    table = Table(header_style="bold cyan", border_style="dim cyan")

    return df_to_table(titles_df, table)


def list_of_winners(league: str):
    """Return DF with the winner each season."""
    path = Path.cwd() / "data/leagues" / league
    files = path.glob("*.txt")

    winners = []

    for file in sorted(files):
        winners.append([file.stem, file.read_text().split("\n")[0]])

    df = DataFrame(winners)
    df.columns = ["Season", "Winner"]
    df["Season"] = df["Season"].str.replace("_", "-")
    table = Table(header_style="bold cyan", border_style="dim cyan")

    return df_to_table(df, table)
