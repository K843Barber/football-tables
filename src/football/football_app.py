from pandas import DataFrame
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Button,
    DataTable,
    Digits,
    Footer,
    Header,
    Label,
    Placeholder,
    Static,
)
from textual_serve.server import Server

from football.__init__ import __version__
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


class MainScreen(ModalScreen):
    BINDINGS = [("escape", "Pop Screen")]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()


class OtherScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Header(name="Football Tables")
        yield Label("Version", classes="version_label")
        yield Digits(__version__, id="version_value")

        with Horizontal(classes="table_container") as right:
            dataframe = FootballDataTable(classes="table")
            dataframe.border_title = "Table"
            right.border_title = f"{self.path.replace("_", " ")} {self.start}-{self.end}"
            yield dataframe
            with VerticalScroll(classes="inner_container") as inner:
                self.wicked_wango = Static("")
                inner.border_title = "Results"
                yield self.wicked_wango

        yield Footer()


class FootballPage(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Football")
        yield Footer()


class StatsPage(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Stats")
        yield Footer()


class ModesApp(App):
    CSS_PATH = "styling.tcss"
    BINDINGS = [
        ("f", "switch_mode('football')", "Football"),
        ("s", "switch_mode('stats')", "Stats"),
    ]

    MODES = {
        "football": FootballPage,
        "stats": StatsPage,
    }

    def on_mount(self) -> None:
        self.switch_mode("football")


class FootballApp(App):
    """Run the app."""

    CSS_PATH = "styling.tcss"

    def __init__(self, df, path, start, end, all_time):
        """Initialise df with data."""
        self.df = df
        self.path = path
        self.start = start
        self.end = end
        self.all_time = all_time

        super().__init__()

    def compose(self) -> ComposeResult:
        """Generate content."""
        yield Header(name="Football Tables")
        yield Label("Version", classes="version_label")
        yield Digits(__version__, id="version_value")

        with Horizontal(classes="table_container") as right:
            dataframe = FootballDataTable(classes="table")
            dataframe.border_title = "Table"
            right.border_title = f"{self.path.replace("_", " ")} {self.start}-{self.end}"
            yield dataframe
            with VerticalScroll(classes="inner_container") as inner:
                self.wicked_wango = Static("")
                inner.border_title = "Results"
                yield self.wicked_wango

        yield Footer()

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

        magic_val = 3

        if not self.all_time:
            try:
                data = read_results(datapoint, self.path, self.start, self.end)
            except FileNotFoundError as e:
                print(e)

            if len(datapoint) > magic_val:
                data = read_results(datapoint, self.path, self.start, self.end)
            else:
                data = ""
        else:
            data = "Can get results with: \
                  \n\n`football get_game league season_start season_end`"

        self.wicked_wango.update(data)


def run_on_server(league: str, start: str, end: str):
    """."""
    server = Server(f"football interactive {league} {start} {end}")
    server.serve()
