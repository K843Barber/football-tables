from rich.console import Console  # noqa: D100
from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Pretty, RadioSet, Static
from textual_plotext import PlotextPlot

from football.helper_functions import (
    generic_read,
    get_goal_graphic,
    get_team_names,
    h2h_datatable,
    more_deets,
    quick_read,
    read_seasons,
    season_data,
)
from football.tui.widgets.the_table import FootballDataTable

console = Console()


class TableScreen(Screen):
    """."""

    def __init__(self, league):
        """."""
        self.league = league
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Header(icon="<-")
        with Horizontal():
            footy_table = FootballDataTable()
            footy_table.border_title = self.league
            yield footy_table
            season_select = RadioSet(*read_seasons(str(self.league)), id="season_select")
            season_select.border_title = "Select Season"
            yield season_select
            self.data = Static(
                "Seasonal Statistics - Select a season to get started",
                id="seasonal_stats",
            )
            yield self.data

        with Horizontal():
            yield Button("Back", id="back", classes="babygotback")

            self.goal_distribution = PlotextPlot(id="goal_dist")
            self.goal_distribution.border_title = "Goal Distribution"
            yield self.goal_distribution

        yield Footer()

    def on_mount(self) -> None:
        """."""
        self.table = self.query_one(FootballDataTable)
        self.table.add_df(quick_read(str(self.league)))
        self.selected_team = ""
        self.shit = ""
        self.start = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "back":
            self.dismiss(True)

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """."""
        self.start, end = str(event.pressed.label).split("_")
        self.table.update_df(generic_read(self.league, self.start, end))
        self.data.update(season_data(self.league, self.start, end))

    def replot(self, team: str, league: str, season: str) -> None:
        """."""
        plt = self.query_one(PlotextPlot).plt
        plt.clear_data()
        self.bollox, key, val = get_goal_graphic(team, league, season)
        plt.bar(key, val)
        plt.yticks(range(0, max(val) + 1, 1))  # type: ignore
        self.refresh()

    @on(FootballDataTable.CellHighlighted)
    def on_cell_selected(self, event: FootballDataTable.CellHighlighted):
        """."""
        self.selected_team = str(event.value)
        if "(" in str(self.selected_team):
            self.selected_team = self.selected_team.split(" (")[0]

        self.shit = self.start
        if self.shit != "":
            self.replot(self.selected_team, self.league, self.shit)
        else:
            self.replot(self.selected_team, self.league, "2024")
        self.goal_distribution.border_title = f"Goal Distribution: {self.selected_team}"


class QuitScreen(Screen):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Grid(
            Static("You wanna Quit?", id="question"),
            Button("Yes", variant="error", id="yes"),
            Button("No", variant="success", id="no"),
            id="quit_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed):
        """."""
        if event.button.id == "yes":
            self.app.exit()
        else:
            self.dismiss(True)


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


class ContentScreen(Screen):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        with Grid():
            yield Button("Tables and Stats", id="Tables")
            yield Button("Head 2 Head", id="h2h")
            yield Button("back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "back":
            self.dismiss(True)
