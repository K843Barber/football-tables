"""Helper functions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from numpy import reshape
from pandas import DataFrame
from textual_serve.server import Server


def get_team_names(league: str) -> list[Any]:
    """Collect team names in each league."""
    p = Path.cwd() / "refined_data" / league
    paths = p.glob("*results.csv")
    total_df = []
    for path in paths:
        total_df.append(DataFrame(pd.read_csv(path)))
    total_df = pd.concat(total_df)

    corrected1 = DataFrame(sorted(set(total_df["Home"].str.replace("\xa0", " "))))  # type: ignore
    corrected1.columns = ["Team"]

    return sorted(set(corrected1["Team"]))


def convert_data_to_df(league: str, season_start: str, season_end: str) -> DataFrame:
    """Convert txt data to dataframe."""
    path = Path.cwd() / "refined_data" / league / f"{season_start}_{season_end}.txt"
    data = list(path.read_text().splitlines())
    data = reshape(data, (int(len(data) / 10), 10))  # type: ignore
    data = DataFrame(
        data, columns=["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    )

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


# print(get_team_names("La_Liga"))
