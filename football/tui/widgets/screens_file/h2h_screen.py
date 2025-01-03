from textual.app import ComposeResult  # noqa: D100
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Pretty, RadioSet, Static

from football.common.h2h_helper import h2h_datatable, more_deets
from football.common.helper_functions import get_team_names


class H2HScreen(Screen):
    """."""

    def __init__(self, league):
        """."""
        self.league = league
        self.doop = Static("", id="button1", classes="team1")
        self.beep = Static("", id="button2", classes="team2")
        self.tits = RadioSet(*get_team_names(self.league), id="button1")
        self.tots = RadioSet(*get_team_names(self.league), id="button2")
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
            with VerticalScroll(classes="base_stats") as wang1:
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
            self.h2h_results.update(
                h2h_datatable(str(self.team1), str(self.team2), self.league)
            )
            self.h2h_stats.update(
                more_deets(str(self.team1), str(self.team2), self.league)
            )
