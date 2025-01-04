"""All time table screen."""

from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, ContentSwitcher, Header, Static

from football.common.all_time_helper import all_time_table, league_winners
from football.common.format_tables import df_to_table
from football.show_table import get_season_list


class AllTime(Screen):
    """."""

    def __init__(self, league):
        """."""
        self.league = league
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Header(name="Football App - All things football: All Time Screen")
        with Horizontal():
            yield Button("All Time Table", id="all_time_willies")
            yield Button("League Wins", id="initbruv")

        with ContentSwitcher(initial="all_time_willies"):
            with VerticalScroll(
                id="all_time_willies", classes="alltimetableframe"
            ) as outer:
                outer.border_title = "All time table"
                table = Table(header_style="bold magenta", border_style="dim magenta")

                seasons = get_season_list(self.league)
                df = all_time_table(self.league, seasons)
                table = df_to_table(df, table)
                yield Static(table, id="all_TT")
            league_wins = league_winners(self.league)
            yield Static(league_wins, id="initbruv")

        yield Button("Back", id="back")

    def on_mount(self):
        """."""
        self.league_selection = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "back":
            self.dismiss(True)
        if event.button.id == "all_time_willies":
            self.query_one(ContentSwitcher).current = event.button.id
        if event.button.id == "initbruv":
            self.query_one(ContentSwitcher).current = event.button.id
