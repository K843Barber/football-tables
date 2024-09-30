from typing import Optional

import pandas as pd
from pandas import concat, DataFrame, merge
from rich import box
from rich.console import Console
from rich.table import Table

from typing import List

console = Console()

def give_dataframe(
        league: str,
        season_start: str,
        season_end: str,
        ) -> DataFrame:
    """
    Converts a standardized txt file into a pd.DataFrame.

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
    except FileNotFoundError("File does not exist"):
        raise FileNotFoundError("File does not exist")

    table = [lines[x:x+10] for x in range(0, len(lines), 10)]
    table = [[i.strip() for i in j] for j in table]

    table1 = []
    for i in table:
        tmp = i[1]
        i[1] = i[0]
        i[0] = tmp
        table1.append(i)

    return DataFrame(table1, columns=['Pos', 'Team', 'Pld', 'W', 'D', 
                                      'L', 'GF', 'GA', 'GD', 'Pts'])



def df_to_table(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    show_index: bool = False,
    index_name: Optional[str] = None,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj.

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
    """Add rich customization to the table.

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
    table.row_styles = ["green",
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
    all_time_table = DataFrame(columns=['Pos', 'Team', 'Pld', 'W', 'D', 
                                      'L', 'GF', 'GA', 'GD', 'Pts'])
    import re
    dfs = []
    for season in seasons:
        print(season)
        if int(season) > 50:
            df = give_dataframe(league, f"19{season}", str(int(season)+1))
        else:
            df = give_dataframe(league, f"20{season}", str(int(season)+1))
        print(df['Team'])
        # df['Team'] = [re.findall(r'[A-Za-z]+', line) for line in df['Team']]
        df['Team'] = df['Team'].str.replace(r'\(.*\)', '', regex=True)
        df['Team'] = df["Team"].str.rstrip(" ")
        print(df['Team'])
        dfs.append(df)

        

    all_time_table = DataFrame(concat(dfs))
    # print(merge(dfs, on="Team", right="Team"))
    all_time_table['Pos'] = all_time_table['Pos'].astype(int)
    all_time_table['Pts'] = all_time_table['Pts'].astype(int)
    all_time_table['Pld'] = all_time_table['Pld'].astype(int)
    all_time_table['W'] = all_time_table['W'].astype(int)
    all_time_table['D'] = all_time_table['D'].astype(int)
    all_time_table['L'] = all_time_table['L'].astype(int)
    all_time_table['GF'] = all_time_table['GF'].astype(int)
    all_time_table['GA'] = all_time_table['GA'].astype(int)
    print(all_time_table)
    new = all_time_table.groupby(by="Team", as_index=False)
    print(DataFrame(new.sum()).sort_values("Pts", ascending=False))
    # print(all_time_table[all_time_table['Team'] == "Manchester United"])


print(all_time_table("Premier_League", ["92","93","94", "19"]))