from matplotlib import table
from rich.console import Console  # noqa: D100
from rich.table import Table
from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    ContentSwitcher,
    Footer,
    Header,
    MarkdownViewer,
    Pretty,
    RadioSet,
    Static,
)
from textual_plotext import PlotextPlot

from football.common.all_time_helper import all_time_table, league_winners
from football.common.format_tables import df_to_table
from football.common.h2h_helper import h2h_datatable, more_deets
from football.common.helper_functions import get_team_names
from football.common.league_page_helper import (
    generic_read,
    get_goal_conceded_graphic,
    get_goal_graphic,
    quick_read,
    read_seasons,
    season_data,
)
from football.common.readme import MARKDOWN
from football.show_table import get_season_list
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
        if self.selected_team in get_team_names(self.league):  # shouldn't need this
            if self.Season != "":  # Update radioset selection and remove this need
                self.replot(self.selected_team, self.league, self.Season)
            else:
                self.replot(self.selected_team, self.league, "2024")
        self.GFD.border_title = f"Goal Distribution: {self.selected_team}"
        self.GAD.border_title = f"Goal Against Distribution: {self.selected_team}"


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
        yield Header()
        yield Grid(
            Button("Tables and Stats", id="Tables"),
            Button("Head 2 Head", id="h2h", classes="H2HINIT"),
            Button("All Time", id="allatida"),
            Button("back", id="back"),
            id="what_we_got",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "back":
            self.dismiss(True)


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
                table = Table()

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


class ReadMeScreen(Screen):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield MarkdownViewer(MARKDOWN, show_table_of_contents=True)
        yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "back":
            self.dismiss(True)
