from rich.console import Console  # noqa: D100
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal
from textual.widgets import Button, Footer, Header, Pretty

from football.helper_functions import read_files
from football.tui.widgets.screens import (
    AllTime,
    ContentScreen,
    H2HScreen,
    QuitScreen,
    TableScreen,
)

console = Console()

welcome_text = """Welcome to the Football App where you can do things like see standings for whichever league you are interested in. Also possible to look at head to head's. Future to look to implement bar chart of frequency of goals scored per game in a season and maybe even over all the collected leagues."""  # noqa: E501


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
        with Horizontal():
            yield Pretty(
                welcome_text,
                id="text",
            )
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
        if event.button.id not in ("back", "quit", "no", "Tables", "h2h", "allatida"):
            self.selected_league = str(event.button.label)
            self.push_screen(ContentScreen())

        if event.button.id == "quit":
            self.push_screen(QuitScreen())
        if event.button.id == "Tables":
            self.push_screen(TableScreen(self.selected_league))
        if event.button.id == "h2h":
            self.push_screen(H2HScreen(self.selected_league))
        if event.button.id == "allatida":
            self.push_screen(AllTime(self.selected_league))
