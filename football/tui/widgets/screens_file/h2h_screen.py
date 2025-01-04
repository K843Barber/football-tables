"""Head 2 Head Screen."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, RadioSet, Static

from football.common.h2h_helper import (
    biggest_win,
    h2h_datatable,
    more_deets,
    win_lose_draw,
)
from football.common.helper_functions import get_team_names


class H2HScreen(Screen):
    """."""

    def __init__(self, league):
        """."""
        self.league = league

        self.tits = RadioSet(*get_team_names(self.league), id="button1")
        self.tots = RadioSet(*get_team_names(self.league), id="button2")
        self.biggest_scoreline = Static()
        self.h2h_results = Static()
        self.h2h_stats = Static()
        self.h2h_outcome = Static()
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
                h2h.border_title = "Biggest Win"
                yield self.biggest_scoreline

            with VerticalScroll(classes="h2h") as team2:
                team2.border_title = "Team 2"
                yield self.tots

        with Horizontal(classes="statistics_container"):
            with VerticalScroll(classes="base_stats") as wang1:
                wang1.border_title = "Results"
                yield self.h2h_results
            with Vertical(classes="base_stats") as wang:
                wang.border_title = "Stats"
                yield self.h2h_stats
            with Vertical(classes="base_stats") as wong:
                wong.border_title = "WDL"

                yield self.h2h_outcome
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
            self.team1 = str(event.pressed.label)
        if event.radio_set.id == "button2":
            self.team2 = str(event.pressed.label)

        if self.team1 and self.team2:
            self.h2h_results.update(h2h_datatable(self.team1, self.team2, self.league))
            self.h2h_stats.update(
                more_deets(self.team1, self.team2, self.league),
            )
            self.h2h_outcome.update(
                win_lose_draw(self.team1, self.team2, self.league),
            )
            self.biggest_scoreline.update(
                biggest_win(self.team1, self.team2, self.league)
            )
