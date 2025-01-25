"""Helper functions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from numpy import reshape
from pandas import DataFrame, Series, concat, read_csv
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
    path = Path.cwd() / "refined_data" / league / f"{start}_{int(start) + 1}.txt"
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


def team_news(team: str, league: str, stat: str) -> tuple[Series, list[int]]:
    """Get team info."""
    path = Path.cwd() / "refined_data" / league
    files = path.glob("*.txt")
    years = [file.stem.split("_")[0] for file in files]

    df = DataFrame()

    years = list(map(int, years))  # type: ignore
    for year in sorted(years):
        df_to_add = query_with_all(convert_data_to_df_mini(league, year), team)
        if df_to_add.empty:
            df_to_add = DataFrame(0, index=[0], columns=df_to_add.columns)
            df_to_add["Team"] = team
            df_to_add["Pos"] = 20

        df = concat([df, df_to_add])
    df["year"] = sorted(years)

    item2 = list(map(int, df[stat]))  # type: ignore
    return df["year"], item2


def try_convert_to_int(value):
    """."""
    try:
        val = float(value)
        if val.is_integer():
            return int(val)
        else:
            return val
    except ValueError:
        return value


def general_stats(team: str, league: str):
    """Get team info."""
    path = Path.cwd() / "refined_data" / league
    files = path.glob("*.txt")
    years = [file.stem.split("_")[0] for file in files]

    df = DataFrame()

    years = list(map(int, years))  # type: ignore
    for year in sorted(years):
        df_to_add = query_with_all(convert_data_to_df_mini(league, year), team)
        if df_to_add.empty:
            df_to_add = DataFrame(0, index=[0], columns=df_to_add.columns)
            df_to_add["Team"] = team
            df_to_add["Pos"] = 20

        df = concat([df, df_to_add])

    df["year"] = sorted(years)
    df = df.reset_index().drop("index", axis=1)
    df["GF"] = list(map(int, df["GF"]))
    df["Pts"] = list(map(int, df["Pts"]))
    df["Pos"] = list(map(int, df["Pos"]))
    df["W"] = list(map(int, df["W"]))
    data = DataFrame(
        {
            "Most goals": df.at[df["GF"].idxmax(), "GF"],
            "Which year": df.at[df["GF"].idxmax(), "year"],
            "Average points per season": sum(df["Pts"]) / len(df["Pts"]),
            "Average goals per season": sum(df["GF"]) / len(df["GF"]),
            "Highest league position": min(df["Pos"]),
            "Most wins in a season": max(df["W"]),
            "Most Points in a season": max(df["Pts"]),
        },
        index=[0],
        dtype=object,
    ).T

    data = data.reset_index()
    data.columns = ["Stat", "Value"]

    return DataFrame(data)
