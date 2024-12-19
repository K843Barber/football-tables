import re  # noqa: D100
from pathlib import Path

import pandas as pd
from numpy import reshape
from pandas import DataFrame, concat
from rich.console import Console
from rich.table import Table

from .format_tables import df_to_table, give_dataframe, enrich_tablev2

console = Console()


def all_time_table(league: str, seasons: list):
    """Give DataFrame with all seasons."""
    cols = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    all_time_table = DataFrame(columns=cols)

    dfs = []
    for season in seasons:
        df = give_dataframe(league, f"{season}", f"{int(season) + 1}")

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


def convert_data_to_df(league: str, season_start: str, season_end: str):
    """Convert txt data to dataframe."""
    path = Path.cwd() / "data" / league / f"{season_start}_{season_end}.txt"
    data = list(path.read_text().splitlines())
    data = reshape(data, (int(len(data) / 10), 10))  # type: ignore
    data = DataFrame(
        data, columns=["Team", "Pos", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    )

    return DataFrame(data)


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


def read_results(team: str, league: str, season_start: str, season_end: str):
    """Gather results and place them on query."""
    path = Path.cwd() / "data" / league / f"{season_start}_{season_end}_results.csv"
    data = pd.read_csv(path)
    home = data[data["Home"] == team]
    away = data[data["Away"] == team]
    table = Table(show_header=False, header_style="bold magenta")
    data = pd.concat([home, away])
    return df_to_table(data, table)


def h2h_datatable(team1: str, team2: str):
    """."""
    data = DataFrame(pd.read_csv("data/Premier_League/2019_2020_results.csv"))
    # data1 = DataFrame(pd.read_csv("data/Premier_League_2023_2024_results.csv"))
    # data2 = DataFrame(pd.read_csv("data/Premier_League_2024_2025_results.csv"))
    # data = pd.concat([data, data1, data2])
    table = Table(show_header=False, header_style="bold magenta")
    data = data[
        (
            ((data["Home"] == team1) & (data["Away"] == team2))
            | ((data["Home"] == team2) & (data["Away"] == team1))
        )
    ]
    if team1 is None or team2 is None:
        return ""
    else:
        return df_to_table(data, table)


def more_deets(team1: str, team2: str):
    """."""
    data = DataFrame(pd.read_csv("data/Premier_League/2019_2020_results.csv"))
    # data1 = DataFrame(pd.read_csv("data/Premier_League_2023_2024_results.csv"))
    # data2 = DataFrame(pd.read_csv("data/Premier_League_2024_2025_results.csv"))
    # data = pd.concat([data, data1, data2])

    table = Table(show_header=True, header_style="bold magenta")
    data = data[
        (
            ((data["Home"] == team1) & (data["Away"] == team2))
            | ((data["Home"] == team2) & (data["Away"] == team1))
        )
    ]

    data["home_score"] = data["Result"].str.split("–")
    df = data["home_score"].apply(pd.Series)
    df.columns = ["Home_score", "Away_score"]
    df1 = data.assign(**df)
    df1 = df1.drop(columns=["Result", "home_score"])
    dfh = DataFrame(df1[["Home", "Home_score"]])
    dfa = DataFrame(df1[["Away", "Away_score"]])
    dfa.columns = ["Home", "Home_score"]
    df1 = DataFrame(pd.concat([dfh, dfa]))
    df1["Home_score"] = pd.to_numeric(df1["Home_score"])
    df_sum = df1.groupby("Home")["Home_score"].sum().reset_index()

    df_sum = df_sum.T
    df_sum.insert(1, "newcol", ["Team", "Goals"])

    # df_sum = df_sum.to_string(header=False)
    if team1 is None or team2 is None:
        return ""
    else:
        return enrich_tablev2(df_sum)


def get_team_names():
    """."""
    data = DataFrame(pd.read_csv("data/Premier_League/2019_2020_results.csv"))
    return sorted(set(data["Home"]))
