"""Helper functions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from numpy import reshape
from pandas import DataFrame, concat, read_csv
from textual_serve.server import Server


def get_team_names(league: str) -> list[Any]:
    """Collect team names in each league."""
    p = Path.cwd() / "refined_data" / league
    paths = p.glob("*results.csv")
    total_df = []
    for path in paths:
        total_df.append(DataFrame(read_csv(path)))
    total_df = concat(total_df)

    return sorted(set(total_df["Home"]))  # type: ignore


def convert_data_to_df(league: str, start: str, end: str) -> DataFrame:
    """Convert txt data to dataframe."""
    path = Path.cwd() / "refined_data" / league / f"{start}_{end}.txt"
    data = list(path.read_text().splitlines())
    x, y = int(len(data) / 10), 10
    data = reshape(data, shape=(x, y))  # type: ignore
    cols = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    data = DataFrame(data, columns=cols)

    data[["Team", "Pos"]] = data[["Pos", "Team"]]  # type: ignore

    return data


def run_on_server() -> None:
    """Run interactive on server."""
    server = Server("football interactive")
    server.serve()


def get_season_list(league: str) -> list:
    """."""
    path = Path.cwd() / "refined_data" / league
    files = path.rglob("*.txt")

    return [file.stem.split("_")[0] for file in files]


def convert_data_to_df_mini(league: str, start: str) -> DataFrame:
    """Convert txt data to dataframe."""
    path = Path.cwd() / "refined_data" / league / f"{start}_{int(start)+1}.txt"
    data = list(path.read_text().splitlines())
    x, y = int(len(data) / 10), 10
    data = reshape(data, shape=(x, y))  # type: ignore
    cols = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    data = DataFrame(data, columns=cols)

    data[["Team", "Pos"]] = data[["Pos", "Team"]]  # type: ignore
    league_table = data

    return league_table


def query_with_all(data_frame, query_string):
    """Nifty little requester thing."""
    if query_string == "all":
        return data_frame
    return data_frame.loc[data_frame["Team"] == query_string]


def team_news(team: str, league: str, stat: str):
    """Get team info."""
    path = Path.cwd() / "refined_data" / league
    files = path.glob("*.txt")
    years = [file.stem.split("_")[0] for file in files]

    df = DataFrame()

    years = list(map(int, years))  # type: ignore
    for year in sorted(years):
        df = concat([df, query_with_all(convert_data_to_df_mini(league, year), team)])
    df["year"] = sorted(years)

    goals = list(map(int, df[stat]))
    return list(df["year"]), goals


team_news("Liverpool", "Premier_League", "Pos")
