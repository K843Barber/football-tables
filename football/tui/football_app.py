from rich.console import Console  # noqa: D100
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, VerticalScroll
from textual.widgets import (
    Button,
    Digits,
    Footer,
    Header,
    Label,
    Static,
)
from textual_serve.server import Server

from football.__init__ import __version__
from football.helper_functions import read_results
from football.tui.screens import (
    Head2HeadPage,
    HomeScreen,
    QuitScreen,
    Standings,
    StatsPage,
)
from football.tui.the_table import FootballDataTable

console = Console()


class FootballAppV2(App):
    """."""

    CSS_PATH = "styling.tcss"
    BINDINGS = [  # noqa: RUF012
        ("t", "push_screen('home')", "home"),
        ("f", "push_screen('standings')", "Standings"),
        ("s", "push_screen('stats')", "Stats"),
        ("h", "push_screen('head2head')", "Head 2 Head"),  # ,
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
        yield Static(
            "[bold cyan]Welcome to my Football Application![/bold cyan]", id="footy_title"
        )
        yield Grid(
            Button("Standings", id="standings"),
            Button("Stats", id="stats"),
            Button("H2H", id="h2h"),
            Button("Quit", id="quit"),
            id="homer",
        )
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
        elif event.button.id == "quit":
            self.push_screen(QuitScreen())


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
