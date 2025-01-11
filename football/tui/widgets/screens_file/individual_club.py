"""."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Input
from textual_plotext import PlotextPlot

from football.common.helper_functions import team_news


class IndividualTeamScreen(Screen):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Header(name="Manchester United")
        with Vertical():
            with Horizontal():
                yield PlotextPlot(id="GF")
            with Horizontal():
                yield PlotextPlot(id="league_pos")

        yield Footer()

    def on_mount(self) -> None:
        """."""
        plt = self.query_one("#GF", PlotextPlot).plt
        x, y = team_news("Arsenal", "Premier_League", "GF")
        plt.bar(x, y, color="cyan", width=0.5)
        plt.show()
        plt1 = self.query_one("#league_pos", PlotextPlot).plt
        x1, y1 = team_news("Arsenal", "Premier_League", "Pos")
        plt1.scatter(
            x1,
            y1,
            marker="X",
        )
        plt1.show()

    # def replot(self, team: str, league: str, season: str) -> None:
    #     """."""
    #     plt = self.query_one("#goal_dist", PlotextPlot).plt
    #     plt.clear_data()
    # _, key, val = get_goal_graphic(team, league, season)
    #     plt.bar(key, val, color="green")
    #     plt.yticks(range(0, max(val) + 1, 1))  # type: ignore

    #     plt1 = self.query_one("#goal_against", PlotextPlot).plt
    #     plt1.clear_data()
    #     _, key, val = get_goal_conceded_graphic(team, league, season)
    #     plt1.bar(key, val, color="red")
    #     plt1.yticks(range(0, max(val) + 1, 1))  # type: ignore

    #     self.refresh()
