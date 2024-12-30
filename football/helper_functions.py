from __future__ import annotations  # noqa: D100

import re
from pathlib import Path
from typing import Any

import pandas as pd
from numpy import reshape
from pandas import DataFrame, concat
from rich.table import Table
from textual_serve.server import Server

from football.format_tables import (
    df_to_table,
    enrich_tablev2,
    enrich_tablev3,
    give_dataframe,
)


def read_results(team: str, league: str, season_start: str, season_end: str) -> Table:
    """Gather results and place them on query."""
    path = Path.cwd() / "data" / league / f"{season_start}_{season_end}_results.csv"
    data = pd.read_csv(path)
    home = data[data["Home"] == team]
    away = data[data["Away"] == team]
    table = Table(show_header=False, header_style="bold magenta")
    data = pd.concat([home, away])
    return df_to_table(data, table)


# H2H Results
def h2h_datatable(team1: str, team2: str, league: str) -> str | Table:
    """Collect results between two teams."""
    path = Path.cwd() / "data" / league
    paths = path.glob("*results.csv")
    total_df = []
    for path in paths:
        total_df.append(DataFrame(pd.read_csv(path)))

    data = pd.concat(total_df)

    table = Table(show_header=False)
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


def more_deets(team1: str, team2: str, league: str) -> str | Table:
    """Collect h2h statistics."""
    path = Path.cwd() / "data" / league
    paths = path.glob("*results.csv")
    total_df = []
    for path in paths:
        total_df.append(DataFrame(pd.read_csv(path)))

    data = pd.concat(total_df)
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
    clean_sheets: dict = {}

    for _, row in df1.iterrows():
        if int(row["Home_score"]) == 0:
            if row["Away"] in clean_sheets:
                clean_sheets[row["Away"]] += 1
            else:
                clean_sheets[row["Away"]] = 1
        if int(row["Away_score"]) == 0:
            if row["Home"] in clean_sheets:
                clean_sheets[row["Home"]] += 1
            else:
                clean_sheets[row["Home"]] = 1

    if team1 not in clean_sheets:
        clean_sheets[team1] = 0
    if team2 not in clean_sheets:
        clean_sheets[team2] = 0

    if team1 is None or team2 is None or df1.empty:
        return ""
    else:
        dfh = DataFrame(df1[["Home", "Home_score"]])
        dfa = DataFrame(df1[["Away", "Away_score"]])
        dfa.columns = ["Home", "Home_score"]
        df1 = DataFrame(pd.concat([dfh, dfa]))
        df1["team_score"] = pd.to_numeric(df1["Home_score"])
        df_sum = df1.groupby("Home")["team_score"].sum().reset_index()

        df_sum = df_sum.T
        df_sum.columns = ["h", "a"]

        df_sum.insert(1, "newcol", ["Team", "Goals"])
        cs = DataFrame(clean_sheets.items()).T

        cs = cs[cs.iloc[0].sort_values(ascending=True).index]
        cs.columns = ["h", "a"]

        cs.insert(1, "newcol", ["Team", "Clean Sheets"])
        stats = pd.concat([df_sum, cs.tail(1)])

        return enrich_tablev2(stats)


def get_team_names(league: str) -> list[Any]:
    """Collect team names in each league."""
    p = Path.cwd() / "data" / league
    paths = p.glob("*results.csv")
    total_df = []
    for path in paths:
        total_df.append(DataFrame(pd.read_csv(path)))

    total_df = pd.concat(total_df)

    return sorted(set(total_df["Home"]))  # type: ignore


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


def season_data(league: str, ss: str, se: str) -> DataFrame:
    """Collect and show league data."""
    df = convert_data_to_df(league, ss, se)
    goal_data = pd.to_numeric(df["GF"])
    total_games = len(goal_data) * len(goal_data) - 1

    new_df = DataFrame(
        {"Goals": sum(goal_data), "Goals per game": f"{sum(goal_data)/total_games:.2f}"},
        index=["0"],
    ).T.reset_index()

    return enrich_tablev3(new_df)


def quick_read(league: str) -> DataFrame:
    """Instantiate league table on first view."""
    ss, se = str(2023), str(2024)
    return convert_data_to_df(league, ss, se)


def generic_read(league: str, ss: str, se: str) -> DataFrame:
    """Update league table with new selection."""
    return convert_data_to_df(league, ss, se)


def read_files() -> list:
    """Collect list of leagues."""
    path = Path.cwd() / "data"
    folders = path.glob("*/")
    leagues = [i.name for i in folders]
    return sorted(leagues)


def read_seasons(league: str) -> list:
    """Collect list of seasons."""
    path = Path.cwd() / "data" / league
    files = path.glob("*.txt")
    seasons = [str(i.name).split(".")[0] for i in files]
    return sorted(seasons)


def run_on_server() -> None:
    """Run interactive on server."""
    server = Server("football interactive")
    server.serve()


def get_goal_graphic(team: str, league: str, start: str):
    """."""
    path = Path.cwd() / "data" / league / f"{start}_{int(start)+1}_results.csv"
    a_ath = pd.read_csv(path)

    df = DataFrame(a_ath)
    df["Home"] = df["Home"].str.replace(" ", " ")
    df["Away"] = df["Away"].str.replace(" ", " ")
    dfh = df[df["Home"] == team]
    dfa = df[df["Away"] == team]

    df1 = pd.concat([dfh, dfa])

    df1["Result"] = df1["Result"].str.replace("−", "–")  # noqa: RUF001
    df1["home_score"] = df1["Result"].str.split("–")  # noqa: RUF001

    goal_dist: dict = {}
    for row in df1.itertuples():
        if row.Home == team:
            if row.home_score[0] in goal_dist:
                goal_dist[row.home_score[0]] += 1
            else:
                goal_dist[row.home_score[0]] = 1
        if row.Away == team:
            if row.home_score[1] in goal_dist:
                goal_dist[row.home_score[1]] += 1
            else:
                goal_dist[row.home_score[1]] = 1

    d = goal_dist
    d = dict(sorted(d.items(), key=lambda item: item[0]))
    keys, value = d.keys(), list(d.values())
    return str(path), keys, value


def get_goal_conceded_graphic(team: str, league: str, start: str):
    """."""
    path = Path.cwd() / "data" / league / f"{start}_{int(start)+1}_results.csv"

    a_ath = pd.read_csv(path)

    df = DataFrame(a_ath)
    df["Home"] = df["Home"].str.replace(" ", " ")
    df["Away"] = df["Away"].str.replace(" ", " ")
    dfh = df[df["Home"] == team]
    dfa = df[df["Away"] == team]

    df1 = pd.concat([dfh, dfa])
    df1["Result"] = df1["Result"].str.replace("−", "–")  # noqa: RUF001
    df1["home_score"] = df1["Result"].str.split("–")  # noqa: RUF001

    goal_dist: dict = {}
    for row in df1.itertuples():
        if row.Home == team:
            if row.home_score[1] in goal_dist:
                goal_dist[row.home_score[1]] += 1
            else:
                goal_dist[row.home_score[1]] = 1
        if row.Away == team:
            if row.home_score[0] in goal_dist:
                goal_dist[row.home_score[0]] += 1
            else:
                goal_dist[row.home_score[0]] = 1

    d = goal_dist
    d = dict(sorted(d.items(), key=lambda item: item[0]))
    keys, value = d.keys(), list(d.values())
    return str(path), keys, value
