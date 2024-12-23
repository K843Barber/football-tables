import re  # noqa: D100
from pathlib import Path

import pandas as pd
from numpy import reshape
from pandas import DataFrame, concat
from rich.table import Table
from textual_serve.server import Server

from football.format_tables import df_to_table, enrich_tablev2, give_dataframe, enrich_tablev3


def read_results(team: str, league: str, season_start: str, season_end: str):
    """Gather results and place them on query."""
    path = Path.cwd() / "data" / league / f"{season_start}_{season_end}_results.csv"
    data = pd.read_csv(path)
    home = data[data["Home"] == team]
    away = data[data["Away"] == team]
    table = Table(show_header=False, header_style="bold magenta")
    data = pd.concat([home, away])
    return df_to_table(data, table)


def h2h_datatable(team1: str, team2: str, league: str):
    """."""
    path = Path.cwd() / "data" / league
    paths = path.glob("*results.csv")
    total_df = []
    for path in paths:
        total_df.append(DataFrame(pd.read_csv(path)))

    data = pd.concat(total_df)

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


def more_deets(team1: str, team2: str, league: str):
    """."""
    path = Path.cwd() / "data" / league
    paths = path.glob("*results.csv")
    total_df = []
    for path in paths:
        total_df.append(DataFrame(pd.read_csv(path)))

    # data = DataFrame(pd.read_csv("data/Premier_League/2019_2020_results.csv"))
    data = pd.concat(total_df)
    # table = Table(show_header=True, header_style="bold magenta")
    data = data[
        (
            ((data["Home"] == team1) & (data["Away"] == team2))
            | ((data["Home"] == team2) & (data["Away"] == team1))
        )
    ]

    data["home_score"] = data["Result"].str.split("–")  # noqa: RUF001

    df = data["home_score"].apply(pd.Series)
    df.columns = ["Home_score", "Away_score"]
    df1 = data.assign(**df)
    df1 = df1.drop(columns=["Result", "home_score"])

    if team1 is None or team2 is None or df1.empty:
        return ""
    else:

        dfh = DataFrame(df1[["Home", "Home_score"]])
        dfa = DataFrame(df1[["Away", "Away_score"]])
        dfa.columns = ["Home", "Home_score"]
        df1 = DataFrame(pd.concat([dfh, dfa]))
        df1["Home_score"] = pd.to_numeric(df1["Home_score"])
        df_sum = df1.groupby("Home")["Home_score"].sum().reset_index()

        df_sum = df_sum.T
        df_sum.insert(1, "newcol", ["Team", "Goals"])
        return enrich_tablev2(df_sum)

        return enrich_tablev2(df_sum)


def get_team_names(league: str) -> set:
    """."""
    paths = Path.cwd() / "data" / league
    paths = paths.glob("*results.csv")
    total_df = []
    for path in paths:
        total_df.append(DataFrame(pd.read_csv(path)))

    total_df = pd.concat(total_df)

    return sorted(set(total_df["Home"]))



def all_time_table(league: str, seasons: list) -> DataFrame:
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


def convert_data_to_df(league: str, season_start: str, season_end: str) -> DataFrame:
    """Convert txt data to dataframe."""
    path = Path.cwd() / "data" / league / f"{season_start}_{season_end}.txt"
    data = list(path.read_text().splitlines())
    data = reshape(data, (int(len(data) / 10), 10))  # type: ignore
    data = DataFrame(
        data, columns=["Team", "Pos", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    )

    return data

def factorial(games: int) -> int:
    if games == 1:
        return games
    else:
        return games * factorial(games-1)


def season_data(l: str, ss: str, se: str) -> DataFrame:
    df = convert_data_to_df(l, ss, se)
    goal_data = pd.to_numeric(df['GF'])
    total_games = (len(goal_data)*len(goal_data)-1)

    new_df = DataFrame({"Goals": sum(goal_data),
                        "Goals per game": f"{sum(goal_data)/total_games:.2f}"}, 
                        index=["0"]).T.reset_index()

    table = Table(title="Seasonal Statistics", 
                  show_header=False, 
                  row_styles=[f"italic{i}" for i in new_df], 
                #   title_style="bold"
                  )

    return enrich_tablev3(new_df)


def quick_read(l: str) -> DataFrame:
    ss, se = 2023, 2024
    return convert_data_to_df(l, ss, se)

def generic_read(l: str, ss: str, se: str) -> DataFrame:
    return convert_data_to_df(l, ss, se)


def read_files() -> list:
    """."""
    path = Path.cwd() / "data"
    folders = path.glob("*/")
    leagues = [i.name for i in folders]
    return sorted(leagues)

def read_seasons(league: str) -> list:
    path = Path.cwd() / "data" / league
    files = path.glob("*.txt")
    seasons = [str(i.name).split(".")[0] for i in files]
    return sorted(seasons)

def run_on_server():
    """."""
    server = Server(f"football interactive")
    server.serve()