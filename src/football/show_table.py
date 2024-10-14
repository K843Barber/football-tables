import re
from typing import List, Optional

import pandas as pd
from pandas import DataFrame, concat
from rich import box
from rich.console import Console
from rich.table import Table

console = Console()


def give_dataframe(
    league: str,
    season_start: str,
    season_end: str,
) -> DataFrame:
    """
    Convert a standardized txt file into a DataFrame.

    Args:
    ----
        league (league): A string given from command line to insert into file to read.
        season_start (season_start): A string given from command line to insert into file
          to read.
        season_end (season_end): A string given from command line to insert into file
        to read.

    Returns:
    -------
        Table: A Pandas DataFrame.

    """
    try:
        with open(f"data/{league}-{season_start}-{season_end}.txt") as f:
            lines = f.readlines()
    except FileNotFoundError():
        print("File does not exist")

    table = [lines[x : x + 10] for x in range(0, len(lines), 10)]
    table = [[i.strip() for i in j] for j in table]

    table1 = []
    for i in table:
        tmp = i[1]
        i[1] = i[0]
        i[0] = tmp
        table1.append(i)

    cols = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]

    return DataFrame(table1, columns=cols)


def df_to_table(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    show_index: bool = False,
    index_name: Optional[str] = None,
) -> Table:
    """
    Convert a pandas.DataFrame obj into a rich.Table obj.

    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
        rich_table (Table): A rich Table that should be populated by the DataFrame values.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults
        to None, showing no value.

    Returns:
        Table: The rich Table instance passed, populated with the DataFrame values.

    """
    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table


def enrich_table(
    datatable: pd.DataFrame,
    league: str,
    season_start: str,
    season_end: str,
) -> None:
    """
    Add rich customization to the table.

    Args:
        datatable: The dataframe to be converted.
        league: league.
        season_start: Year season started.
        season_end: Year season ended.

    """
    # rich table version
    # Initiate a Table instance to be modified
    table = Table(show_header=True, header_style="bold magenta")

    # Modify the table instance to have the data from the DataFrame
    table = df_to_table(datatable, table)

    # Update the style of the table
    table.row_styles = [
        "green",
        "green",
        "green",
        "green",
        "orange3",
        "orange3",
        "orange3",
        "white",
        "white",
        "white",
        "white",
        "white",
        "white",
        "white",
        "white",
        "white",
        "white",
        "red",
        "red",
        "red",
    ]
    table.box = box.DOUBLE_EDGE
    table.title = f"{league} {season_start}-{season_end}"

    console.print(table)


def all_time_table(league: str, seasons: List):
    cols = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    all_time_table = DataFrame(columns=cols)

    dfs = []
    marker = 50
    for season in seasons:
        if int(season) > marker:
            df = give_dataframe(league, f"19{season}", str(1900 + int(season) + 1)[-2:])
        else:
            df = give_dataframe(league, f"20{season}", str(2000 + int(season) + 1)[-2:])

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

    console.print(df)
