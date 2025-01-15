"""League page helper."""

from pathlib import Path

import pandas as pd
from pandas import DataFrame, read_csv

from football.common.format_tables import enrich_tablev3
from football.common.helper_functions import convert_data_to_df


def quick_read(league: str) -> DataFrame:
    """Instantiate league table on first view."""
    return convert_data_to_df(league, str(2024), str(2025))


def generic_read(league: str, ss: str, se: str) -> DataFrame:
    """Update league table with new selection."""
    return convert_data_to_df(league, ss, se)


def read_folders() -> list:
    """Collect list of leagues."""
    path = Path.cwd() / "refined_data"
    folders = path.glob("*/")
    leagues = [i.name for i in folders]
    return sorted(leagues)


def read_seasons(league: str) -> list:
    """Collect list of seasons."""
    path = Path.cwd() / "refined_data" / league
    files = path.glob("*.txt")
    seasons = [str(i.name).split(".")[0] for i in files]
    return sorted(seasons)


def season_data(league: str, ss: str, se: str) -> DataFrame:
    """Collect and show league data in fancy format."""
    df = convert_data_to_df(league, ss, se)
    goal_data = pd.to_numeric(df["GF"])
    g1 = int(sum(pd.to_numeric(df["Pld"])) / 2)

    total_games = g1

    path = Path.cwd() / "refined_data" / league / f"{ss}_{se}_results.csv"
    df_results = DataFrame(pd.read_csv(path))

    home = df_results.loc[df_results["HS"] == 0].shape[0]
    away = df_results.loc[df_results["AS"] == 0].shape[0]

    new_df = DataFrame(
        {
            "Goals": sum(goal_data),
            "Goals per game": f"{sum(goal_data) / total_games:.2f}",
            "Clean Sheets": home + away,
        },
        index=["0"],
    ).T.reset_index()

    return enrich_tablev3(new_df)


def get_goal_graphic(team: str, league: str, start: str):
    """."""
    df1, path = score_df(team, league, start)

    goal_dist: dict = {}
    for row in df1.itertuples():
        if row.Home == team:
            if row.HS in goal_dist:
                goal_dist[row.HS] += 1
            else:
                goal_dist[row.HS] = 1
        if row.Away == team:
            if row.AS in goal_dist:
                goal_dist[row.AS] += 1
            else:
                goal_dist[row.AS] = 1

    d = goal_dist
    d = dict(sorted(d.items(), key=lambda item: item[0]))
    keys, value = d.keys(), list(d.values())

    return str(path), keys, value


def get_goal_conceded_graphic(team: str, league: str, start: str):
    """."""
    df1, path = score_df(team, league, start)

    goal_dist: dict = {}
    for row in df1.itertuples():
        if row.Home == team:
            if row.AS in goal_dist:
                goal_dist[row.AS] += 1
            else:
                goal_dist[row.AS] = 1
        if row.Away == team:
            if row.HS in goal_dist:
                goal_dist[row.HS] += 1
            else:
                goal_dist[row.HS] = 1

    d = goal_dist
    d = dict(sorted(d.items(), key=lambda item: item[0]))
    keys, value = d.keys(), list(d.values())

    return str(path), keys, value


def score_df(team: str, league: str, start: str):
    """."""
    path = Path.cwd() / "refined_data" / league / f"{start}_{int(start) + 1}_results.csv"
    df = DataFrame(pd.read_csv(path))

    dfh = df[df["Home"] == team]
    dfa = df[df["Away"] == team]

    df1 = pd.concat([dfh, dfa])
    return df1, path


def goal_game_distribution(league: str, s: int):
    """."""
    file = Path.cwd() / "refined_data" / league / f"{s}_{s + 1}_results.csv"

    data = read_csv(file)

    data["AG"] = data["HS"] + data["AS"]
    ag = list(data["AG"])

    df: dict = {}
    for i in ag:
        if i not in df:
            df[i] = 1
        else:
            df[i] += 1

    d = df
    d = dict(sorted(d.items(), key=lambda item: item[0]))
    keys, value = d.keys(), list(d.values())

    # df1 = DataFrame(df, index=[0]).T
    # df1 = df1.reset_index()

    # df1.columns = ["Goals", "Frequency"]
    # df1 = df1.sort_values(by=["Goals"])
    return keys, value


# goal_game_distribution("Premier_League", 2024)
