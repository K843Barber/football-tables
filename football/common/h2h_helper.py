from pathlib import Path  # noqa: D100

import pandas as pd
from pandas import DataFrame
from rich.table import Table

from football.common.format_tables import df_to_table, enrich_tablev2


def results_df(team1: str, team2: str, league: str):
    """."""
    path = Path.cwd() / "refined_data" / league
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
    return data, team1, team2


# H2H Results
def h2h_datatable(team1: str, team2: str, league: str) -> str | Table:
    """Collect results between two teams."""
    data, team1, team2 = results_df(team1, team2, league)

    table = Table(show_header=False)

    if team1 is None or team2 is None:
        return ""
    else:
        return df_to_table(data, table)


def more_deets(team1: str, team2: str, league: str) -> str | Table:
    """Collect h2h statistics."""
    data, team1, team2 = results_df(team1, team2, league)
    clean_sheets: dict = {}
    for _, row in data.iterrows():
        if int(row["HS"]) == 0:
            if row["Away"] in clean_sheets:
                clean_sheets[row["Away"]] += 1
            else:
                clean_sheets[row["Away"]] = 1
        if int(row["AS"]) == 0:
            if row["Home"] in clean_sheets:
                clean_sheets[row["Home"]] += 1
            else:
                clean_sheets[row["Home"]] = 1

    if team1 not in clean_sheets:
        clean_sheets[team1] = 0
    if team2 not in clean_sheets:
        clean_sheets[team2] = 0

    if team1 is None or team2 is None or data.empty:
        return ""
    else:
        dfh = DataFrame(data[["Home", "HS"]])
        dfa = DataFrame(data[["Away", "AS"]])
        dfa.columns = ["Home", "HS"]
        df1 = DataFrame(pd.concat([dfh, dfa]))
        df1["Score"] = pd.to_numeric(df1["HS"])
        df_sum = df1.groupby("Home")["Score"].sum().reset_index()

        df_sum = df_sum.T
        df_sum.columns = ["h", "a"]

        df_sum.insert(1, "newcol", ["Team", "Goals"])
        cs = DataFrame(clean_sheets.items()).T

        cs = cs[cs.iloc[0].sort_values(ascending=True).index]
        cs.columns = ["h", "a"]

        cs.insert(1, "newcol", ["Team", "Clean Sheets"])
        stats = pd.concat([df_sum, cs.tail(1)])

        return enrich_tablev2(stats)


# more_deets("AC Milan", "Internazionale", "Serie_A")
