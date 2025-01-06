"""Convert dataframe to rich table."""

from typing import Optional

from pandas import DataFrame
from rich import box
from rich.console import Console
from rich.table import Table

console = Console()


def df_to_table(
    pandas_dataframe: DataFrame,
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
    datatable: DataFrame, league: str, start: str, end: str, stylings
) -> None:  # Make singular and add styles in options
    """Add rich customization to the table.

    Args:
        datatable: The dataframe to be converted.
        league: league.
        start: Year season started.
        end: Year season ended.
        stylings: List of styles.

    """
    # rich table version
    # Initiate a Table instance to be modified
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="dim cyan",
        title_style="magenta",
    )

    # Modify the table instance to have the data from the DataFrame
    table = df_to_table(datatable, table)

    # Update the style of the table
    table.row_styles = stylings
    end = end[2:]
    table.box = box.DOUBLE_EDGE
    table.title = f"{league} {start}-{end}"

    console.print(table, justify="center")


def enrich_tablev2(
    datatable: DataFrame,
) -> Table:
    """Add rich customization to the table.

    Args:
        datatable: The dataframe to be converted.
        league: league.
        season_start: Year season started.
        season_end: Year season ended.

    """
    # rich table version
    # Initiate a Table instance to be modified
    table = Table(show_header=False, border_style="dim magenta")

    # Modify the table instance to have the data from the DataFrame
    table = df_to_table(datatable, table)

    table.box = box.DOUBLE_EDGE

    return table


def enrich_tablev3(
    datatable: DataFrame,
) -> Table:
    """Add rich customization to the table.

    Args:
        datatable: The dataframe to be converted.
        league: league.
        season_start: Year season started.
        season_end: Year season ended.

    """
    table = Table(show_header=False)
    table = df_to_table(datatable, table)

    table.box = box.DOUBLE_EDGE
    table.row_styles = ["purple" for _ in table.rows]
    table.title = "Seasonal Statistics"
    return table


def enrich_tablev4(datatable: DataFrame, title: str = "") -> Table:
    """Add rich customization to the table.

    Args:
        datatable: The dataframe to be converted.
        title: title.

    """
    table = Table(border_style="dim cyan", header_style="bold cyan", title=title)
    table = df_to_table(datatable, table)
    table.box = box.DOUBLE_EDGE

    return table
