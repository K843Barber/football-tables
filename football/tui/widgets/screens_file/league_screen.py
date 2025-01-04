"""League Table screen."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, RadioSet, Static
from textual_plotext import PlotextPlot

from football.common.helper_functions import get_team_names
from football.common.league_page_helper import (
    generic_read,
    get_goal_conceded_graphic,
    get_goal_graphic,
    quick_read,
    read_seasons,
    season_data,
)
from football.tui.widgets.the_table import FootballDataTable


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
            with VerticalScroll(id="season_select") as outer:
                season_select = RadioSet(*read_seasons(str(self.league)))
                outer.border_title = "Select Season"
                yield season_select
            self.data = Static(
                "Seasonal Statistics - Select a season to get started",
                id="seasonal_stats",
            )
            with Vertical():
                yield self.data
                yield Button("Back", id="back", classes="babygotback")

        with Horizontal():
            self.GFD = PlotextPlot(id="goal_dist")
            self.GFD.border_title = "Goal Distribution"
            yield self.GFD
            self.GAD = PlotextPlot(id="goal_against")
            self.GAD.border_title = "Goal Against Distribution"
            yield self.GAD

        yield Footer()

    def on_mount(self) -> None:
        """."""
        self.table = self.query_one(FootballDataTable)
        self.table.add_df(quick_read(str(self.league)))
        self.selected_team = ""
        self.Season = ""
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
        plt = self.query_one("#goal_dist", PlotextPlot).plt
        plt.clear_data()
        _, key, val = get_goal_graphic(team, league, season)
        plt.bar(key, val, color="green")
        plt.yticks(range(0, max(val) + 1, 1))  # type: ignore

        plt1 = self.query_one("#goal_against", PlotextPlot).plt
        plt1.clear_data()
        _, key, val = get_goal_conceded_graphic(team, league, season)
        plt1.bar(key, val, color="red")
        plt1.yticks(range(0, max(val) + 1, 1))  # type: ignore

        self.refresh()

    @on(FootballDataTable.CellHighlighted)
    def on_cell_selected(self, event: FootballDataTable.CellHighlighted):
        """."""
        self.selected_team = str(event.value)

        self.Season = self.start
        if self.selected_team in get_team_names(self.league):
            if self.Season != "":  # Update radioset selection and remove this need
                self.replot(self.selected_team, self.league, self.Season)
            else:
                self.replot(self.selected_team, self.league, "2024")
        self.GFD.border_title = f"Goal Distribution: {self.selected_team}"
        self.GAD.border_title = f"Goal Against Distribution: {self.selected_team}"
