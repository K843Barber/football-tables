"""App main page."""

from rich.console import Console
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal
from textual.widgets import Button, Footer, Header, Pretty

from football.common.league_page_helper import read_folders
from football.tui.widgets.screens_file.all_time_screen import AllTime
from football.tui.widgets.screens_file.h2h_screen import H2HScreen
from football.tui.widgets.screens_file.individual_club import ClubScreen
from football.tui.widgets.screens_file.league_screen import TableScreen
from football.tui.widgets.screens_file.screens import (
    ContentScreen,
    QuitScreen,
    ReadMeScreen,
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
        starter = Grid(id="main_left")
        starter.border_title = "Start Page"
        with Horizontal():
            with starter:
                yield Pretty("Football statistics!", id="text")
                yield Button("README", id="readme")
                yield Button("Quit", id="quit")
            with leagues:
                for league in read_folders():
                    yield Button(league)
        yield Footer()

    def on_mount(self) -> None:
        """."""
        self.title = "Football App"
        self.sub_title = "All things football"
        self.selected_league = ""

    def on_button_pressed(self, event: Button.Pressed):
        """."""
        if event.button.id not in (
            "back",
            "quit",
            "no",
            "Tables",
            "h2h",
            "allatida",
            "All Time Table",
            "League Wins",
            "all_TT",
            "initbruv",
            "all_time_willies",
            "readme",
            "invidual_team",
            "winnerbyseason",
        ):
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
        if event.button.id == "readme":
            self.push_screen(ReadMeScreen())
        if event.button.id == "invidual_team":
            self.push_screen(ClubScreen(self.selected_league))
