"""League page helper."""

from pathlib import Path

import pandas as pd
from pandas import DataFrame

from football.common.format_tables import enrich_tablev3
from football.common.helper_functions import convert_data_to_df


def quick_read(league: str) -> DataFrame:
    """Instantiate league table on first view."""
    return convert_data_to_df(league, str(2024), str(2025))


def generic_read(league: str, ss: str, se: str) -> DataFrame:
    """Update league table with new selection."""
    return convert_data_to_df(league, ss, se)


def read_files() -> list:
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
    total_games = len(goal_data) * len(goal_data) - 1

    new_df = DataFrame(
        {"Goals": sum(goal_data), "Goals per game": f"{sum(goal_data)/total_games:.2f}"},
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
    path = Path.cwd() / "refined_data" / league / f"{start}_{int(start)+1}_results.csv"

    df = DataFrame(pd.read_csv(path))

    dfh = df[df["Home"] == team]
    dfa = df[df["Away"] == team]

    df1 = pd.concat([dfh, dfa])

    return df1, path


# get_goal_graphic("Paris Saint-Germain", "Ligue_1", "2024")
# get_goal_conceded_graphic("Celta Vigo", "La_Liga", "2004")
