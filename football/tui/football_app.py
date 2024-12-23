from rich.console import Console  # noqa: D100
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import (
    Button,
    Footer,
    Header,
)

from football.__init__ import __version__
from football.helper_functions import read_files
from football.tui.screens import (
    ContentScreen,
    H2HScreen,
    QuitScreen,
    TableScreen,
)

console = Console()

class FootballApp(App):
    """."""

    CSS_PATH = "st.tcss"

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Header()
        leagues = Grid(id="grid_box")
        leagues.border_title = "Select a league"
        with leagues:
            for league in read_files():
                yield Button(league)
            yield Button("Quit", id="quit")
        yield Footer()

    def on_mount(self) -> None:
        """."""
        self.title = "Football App"
        self.sub_title = "All things football"
        self.selected_league = ""

    def on_button_pressed(self, event: Button.Pressed):
        """."""
        if event.button.id not in ("back", "quit", "no", "Tables", "h2h"):
            self.selected_league = str(event.button.label)
            self.push_screen(ContentScreen())

        if event.button.id == "quit":
            self.push_screen(QuitScreen())

        if event.button.id == "Tables":
            self.push_screen(TableScreen(self.selected_league))
        if event.button.id == "h2h":
            self.push_screen(H2HScreen(self.selected_league))
