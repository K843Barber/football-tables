"""Club screen."""

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, RadioSet, Static
from textual_plotext import PlotextPlot

from football.common.format_tables import enrich_tablev2
from football.common.helper_functions import general_stats, get_team_names, team_news


class ClubScreen(Screen):
    """."""

    def __init__(self, league):
        """."""
        self.league = league
        self.tits = RadioSet(*get_team_names(self.league))
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Header(icon="<-")
        with VerticalScroll(id="ClubPage") as outer:
            outer.border_title = "Statistics"
            self.team_name = Input(placeholder="Team")
            yield self.team_name

            self.GFD = PlotextPlot(id="GF")
            self.GFD.border_title = "Goals Scored"
            yield self.GFD

            self.lp = PlotextPlot(id="league_pos")
            self.lp.border_title = "League Position"
            yield self.lp

            yield Static()
        yield Button("Back", id="back", classes="babygotback")

        yield Footer()

    async def on_mount(self) -> None:
        """."""
        self.selected_team = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "back":
            self.dismiss(True)

    def replot(self, team: str) -> None:
        """."""
        plt = self.query_one("#GF", PlotextPlot).plt
        plt.clear_data()
        key, val = team_news(team, self.league, "GF")
        plt.bar(key, val, color="green")
        key2, val2 = team_news(team, self.league, "GA")
        plt.bar(key2, val2, color="blue")
        plt.yticks(range(0, max(val) + 1, 1))  # type: ignore
        plt.xlabel("Year")
        plt.ylabel("Goals")

        plt1 = self.query_one("#league_pos", PlotextPlot).plt
        plt1.clear_data()
        key, val = team_news(team, self.league, "Pos")
        plt1.scatter(key, val, color="cyan", marker="X")
        plt1.xticks(range(min(key), max(key) + 1, 1))  # type: ignore
        plt1.yticks(range(0, max(val) + 1, 1))  # type: ignore
        plt1.xlabel("Year")
        plt1.ylabel("League Pos")

        self.refresh()

    def on_input_submitted(self, event: Input.Submitted):
        """."""
        self.team_name = str(event.value)  # type: ignore
        self.replot(self.team_name)  # type: ignore
        self.GFD.border_title = f"Goals Scored: {self.team_name}"
        self.lp.border_title = f"League Position: {self.team_name}"
        self.query_one(Static).update(
            enrich_tablev2(general_stats(self.team_name, self.league))  # type: ignore
        )
        self.query_one(Input).value = ""

    @on(RadioSet.Changed)
    def on_radio_set_changed(self, event: RadioSet.Changed):
        """."""
        self.replot(str(event.pressed.label))
        self.GFD.border_title = "Goals Scored"
        self.lp.border_title = "League Position"
