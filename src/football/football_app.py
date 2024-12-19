from pandas import DataFrame  # noqa: D100
from rich.console import Console
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    DataTable,
    Digits,
    Footer,
    Header,
    Label,
    Pretty,
    RadioSet,
    Static,
)
from textual_serve.server import Server

from football.__init__ import __version__
from football.show_table import get_team_names, h2h_datatable, more_deets, read_results

console = Console()


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


class Standings(Screen):
    """."""

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
            right.border_title = f"{self.path.replace('_', ' ')} {self.start}-{self.end}"
            yield dataframe
            with VerticalScroll(classes="inner_container") as inner:
                self.wicked_wango = Static("")
                inner.border_title = "Results"
                yield self.wicked_wango

        yield Button("Take me back", id="meny")
        yield Footer()

    def _on_mount(self) -> None:
        table = self.query_one(FootballDataTable)
        table.add_df(self.df)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "meny":
            self.dismiss(True)

    @on(FootballDataTable.CellHighlighted)
    async def on_cell(self, event: FootballDataTable.CellHighlighted) -> None:
        """Update results on cell highlight."""
        datapoint = str(event.value)

        if "(C)" in datapoint or "(R)" in datapoint:
            datapoint = datapoint.split("(")[0].strip()

        magic_val = 3

        if not self.all_time:
            try:
                data = read_results(datapoint, self.path, self.start, self.end)
            except FileNotFoundError as e:
                console.print(
                    "[bold red]No results![/bold red]\
                        [bold green]Use get_game[/bold green]",
                    e,
                )

            if len(datapoint) > magic_val:
                data = read_results(datapoint, self.path, self.start, self.end)
            else:
                data = ""
        else:
            data = "Can get results with: \
                  \n\n`football get_game league season_start season_end`"

        self.wicked_wango.update(data)


class StatsPage(Screen):
    """."""

    dff = DataFrame({"A": [1, 2, 3], "B": [34, 34, 456]})

    def compose(self) -> ComposeResult:
        """."""
        with Horizontal(classes="inner_container") as outer:
            outer.border_title = "basic stats"
            df1 = Pretty(self.dff)
            yield df1
        yield Button("Take me back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        """."""
        if event.button.id == "back":
            self.dismiss(True)


class Head2HeadPage(Screen):
    """."""

    def __init__(self):
        """."""
        self.doop = Static("", id="button1", classes="team1")
        self.beep = Static("", id="button2", classes="team2")
        self.tits = RadioSet(*get_team_names(), id="button1")
        self.tots = RadioSet(*get_team_names(), id="button2")
        self.h2h_results = Static("")
        self.h2h_stats = Static()
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Header(name="Welcome to Head 2 Head section", show_clock=True)
        with Horizontal(classes="h2h_container") as outer:
            outer.border_title = "Head 2 Head"

            with VerticalScroll(classes="h2h") as team1:
                team1.border_title = "Team 1"
                yield self.tits

            with Horizontal(classes="h2h") as h2h:
                h2h.border_title = "H2H"
                with Vertical(classes="team1"):
                    yield self.doop
                with Vertical(classes="team2"):
                    yield self.beep

            with VerticalScroll(classes="h2h") as team2:
                team2.border_title = "Team 2"
                yield self.tots

        with Horizontal(classes="statistics_container"):
            with Vertical(classes="base_stats") as wang1:
                wang1.border_title = "Results"
                yield self.h2h_results
            with Vertical(classes="base_stats") as wang:
                wang.border_title = "Stats"
                yield self.h2h_stats
            with Vertical(classes="base_stats") as wong:
                wong.border_title = "Teams"

                yield Pretty(
                    "Maybe add filters here for season if main screen just chooses league"
                )
        yield Button("Take me Back", id="back")
        yield Footer()

    def on_mount(self):
        """."""
        self.team1 = None
        self.team2 = None

    def on_button_pressed(self, event: Button.Pressed):
        """."""
        if event.button.id == "back":
            self.dismiss(True)

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """."""
        if event.radio_set.id == "button1":
            self.team1 = event.pressed.label
            self.query_one("#button1", Static).update(self.team1)
        if event.radio_set.id == "button2":
            self.team2 = event.pressed.label
            self.query_one("#button2", Static).update(self.team2)

        if self.team1 and self.team2:
            self.h2h_results.update(h2h_datatable(str(self.team1), str(self.team2)))
            self.h2h_stats.update(more_deets(str(self.team1), str(self.team2)))


class QuitScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Button("Quit", variant="error", id="quit")
        yield Button("Cancel", variant="primary", id="cancel")

    def on_button_pressed(self, event:Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)

class HomeScreen(Screen):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Header(name="Barry")
        yield Button("Standings", id="standings")
        yield Button("Stats", id="stats")
        yield Button("H2H", id="h2h")
        yield Button("Quit", id="quit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        """."""
        if event.button.id == "standings":
            self.dismiss(True)
        elif event.button.id == "stats":
            self.dismiss(True)
        elif event.button.id == "h2h":
            self.dismiss(True)
        elif event.button.id == "quit":
            self.dismiss(True)


class FootballAppV2(App):
    """."""

    CSS_PATH = "styling.tcss"
    BINDINGS = [  # noqa: RUF012
        ("t", "push_screen('home')", "home"),
        ("f", "push_screen('standings')", "Standings"),
        ("s", "push_screen('stats')", "Stats"),
        ("h", "push_screen('head2head')", "Head 2 Head"),
        ("q", "request_quit", "Quit")
        ]

    def __init__(self, df, path, start, end, all_time):
        """Initialise df with data."""
        self.df = df
        self.path = path
        self.start = start
        self.end = end
        self.all_time = all_time
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        # yield Placeholder("Click a screen (bottom left)")
        yield Button("Standings", id="standings")
        yield Button("Stats", id="stats")
        yield Button("H2H", id="h2h")
        yield Button("Quit", id="quit")
        yield HomeScreen()
        yield Footer()

    def on_mount(self) -> None:
        """."""
        self.install_screen(HomeScreen(), name="home")
        self.install_screen(
            Standings(self.df, self.path, self.start, self.end, self.all_time),
            name="standings",
        )
        self.install_screen(StatsPage(), name="stats")
        self.install_screen(Head2HeadPage(), name="head2head")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "standings":
            self.push_screen(
                Standings(self.df, self.path, self.start, self.end, self.all_time)
            )
        elif event.button.id == "stats":
            self.push_screen(StatsPage())
        elif event.button.id == "h2h":
            self.push_screen(Head2HeadPage())

    def action_request_quit(self) -> None:
        def check_quit(quit: bool | None) -> None:
            if quit:
                self.exit()

        self.push_screen(QuitScreen(), check_quit)

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
            right.border_title = f"{self.path.replace('_', ' ')} {self.start}-{self.end}"
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
