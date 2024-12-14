from tkinter import S
from pandas import DataFrame
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, HorizontalScroll
from textual.widgets import DataTable, Static
from textual_serve.server import Server
from football.show_table import read_results


class FootballDataTable(DataTable):
    """Format football df."""

    def add_df(self, df: DataFrame):
        """Get the df."""
        self.df = df
        self.add_columns(*self._add_df_columns())
        self.add_rows(self._add_df_rows()[0:])
        return self

    def update_df(self, df: DataFrame):
        """Update df."""
        self.clear(columns=True)
        self.add_df(df)

    def _add_df_rows(self):
        return self._get_df_rows()

    def _add_df_columns(self):
        return self._get_df_columns()

    def _get_df_rows(self):
        return list(self.df.itertuples(index=False, name=None))

    def _get_df_columns(self) -> tuple:
        return tuple(self.df.columns.values.tolist())


class FootballApp(App):
    """Run the app."""

    CSS_PATH = "styling.tcss"

    def __init__(self, df, path, start, end):
        """Initialise df with data."""
        self.df = df
        self.path = path
        self.start = start
        self.end = end
        super().__init__()

    def compose(self) -> ComposeResult:
        """Generate content."""
        with Horizontal(classes="table_container") as right:
            dataframe = FootballDataTable(classes="table")
            dataframe.border_title = "Table"
            yield dataframe
            right.border_title = f"{self.path.replace("_", " ")} {self.start}-{self.end}"
            with HorizontalScroll(classes="inner_container") as inner:
                self.wicked_wango = Static("")
                inner.border_title = "Results"
                yield self.wicked_wango

    def on_mount(self):
        """Add df when starting up."""
        table = self.query_one(FootballDataTable)
        table.add_df(self.df)

    @on(FootballDataTable.CellHighlighted)
    async def on_cell(self, event: FootballDataTable.CellHighlighted):
        """Update results on cell hihglight."""
        datapoint = str(event.value)

        if "(C)" in datapoint or "(R)" in datapoint:
            datapoint = datapoint.split("(")[0].strip()
        if len(datapoint) > 3:
            data = read_results(datapoint, self.path, self.start, self.end)
        else:
            data = ""

        self.wicked_wango.update(data)


def run_on_server(league: str, start: str, end: str):
    """."""
    server = Server(f"football interactive {league} {start} {end}")
    server.serve()
