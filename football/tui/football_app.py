"""App main page."""

import os
import sys

from rich.console import Console
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal
from textual.widgets import Button, Footer, Header, Placeholder, Pretty

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


def resource_path(relative_path) -> str:
    """."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)


class FootballApp(App):
    """The football app."""

    # CSS_PATH = resource_path("football/tui/st.tcss")
    CSS = """# ---------------------- Global  ----------------------
        /* The button class */
        Button {
            width: 1fr;
            content-align: center middle;
        }
        ContentSwitcher {
            width: 100%;
            height: 8fr;
        }
        Grid {
            align: center middle;
        }
        # ---------------------- Football Data Screen ----------------------
        FootballDataTable {
            border: solid round orange;
            height:auto;
            width: auto;
        }
        #normal_dist {
            border: solid magenta;
        }
        #season_select {
            border: solid blue;
            width: 20;
        }
        #seasonal_stats {
            border: solid round aqua;
            width: 1fr;
        }
        #goal_dist {
            border: solid round green;
            width: 1fr;
        }
        #goal_against {
            border: solid round red;
            width: 1fr;
        }

        # ---------------------- Quit Screen ----------------------
        QuitScreen {
            align: center middle;
        }
        #question {
            column_span: 2;
            height: 1fr;
            width: 1fr;
            content-align: center middle;
        }
        #quit_dialog {
            grid-size: 2;
            grid-gutter: 1 2;
            grid-rows: 1fr 3;
            padding: 0 1;
            width: 60;
            height: 11;
            border: thick $background 80%;
            background: $surface;
        }
        # ---------------------- Main Screen ----------------------
        #grid_box {
            border: solid magenta;
            width: 50%;
            height: 1fr;
            padding: 0 10;
        }
        # ---------------------- h2h ----------------------
        .h2h {
            border: solid round cyan;
            height: 1fr;
            width: 1fr;
        }
        .h2h_container {
            border: solid round magenta;
            height: 15;
            width: auto;
        }
        .statistics_container {
            width: 1fr;
            height: 15;
            border: solid round cyan;
        }
        .results_container {
            width: 50;
            height: 20;
            border: solid round green;
        }
        .base_stats {
            border: solid aqua;
        }

        # -------------- LeagueScreen/IndividualScreen -------------------
        .babygotback {
            width: 1fr;
            content-align: center middle;
            border: solid magenta;
        }
        # ---------------------- Content Screen ----------------------
        #what_we_got {
            height: 100%;
            margin: 3 40;
            background: $panel;
            color: $text;
            border: tall $background;
            padding: 1 1;
        }
        #Tables {
            background: blue;
            width: 100%;
            color: black;
        }
        .Tables {
            content-align: center middle;
        }
        .H2HINIT {
            background: blue;
            width: 100%;
            content-align: center middle;
            color: black;
        }
        #allatida {
            background: blue;
            color: black;
        }
        #back {
            background: blue;
            width: 100%;
            color: black;
        }
        # -------------------- App Page --------------------
        #main_left {
            content-align: center middle;
            width: 50%;
            height: 1fr;
            padding: 0 10;
            border: solid cyan;
        }
        #text {
            width: 100%;
        }
        # ------------------ All Time Screen ------------------
        #all_TT {
            content-align: center middle;
        }
        #initbruv {
            content-align: center middle;
        }
        #winnerbyseason {
            content-align: center middle;
        }
        .alltimetableframe {
            height: 1fr;
            border: solid magenta;
        }
        # ---------------- club page ------------------
        #ClubPage {
            border: solid green;
        }
        #GF {
            border: solid round cyan;
            height: 20;
        }
        #league_pos {
            border: solid round green;
            width: 1fr;
            height: 20;
        }
        # ---------------- test ------------------

        """

    def __init__(self):
        """."""
        super().__init__()
        # self.CSS_PATH = resource_path("football/tui/st.tcss")

    def compose(self) -> ComposeResult:
        """."""
        yield Header()
        leagues = Grid(id="grid_box")
        leagues.border_title = "Select a league"
        starter = Grid(id="main_left")
        starter.border_title = "Start Page"
        with Horizontal():
            with starter:
                yield Placeholder("Football statistics!", id="text")
                yield Button("README", id="readme")
                yield Button("Quit", id="quit")
            with leagues:
                for league in read_folders():
                    yield Button(league)
        yield Footer()

    def on_mount(self) -> None:
        """."""
        # self.load_css_path(self.CSS_PATH)
        self.title = "Football App"
        self.sub_title = "All things football"
        self.selected_league = ""
        # print(f"Resolved CSS path: {css_path}")
        # await self.stylesheet.read(str(css_path))

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
