# # # class FootballAppV2(App):
# # #     """."""

# # #     CSS_PATH = "styling.tcss"
# # #     BINDINGS = [  # noqa: RUF012
# # #         ("t", "push_screen('home')", "home"),
# # #         ("f", "push_screen('standings')", "Standings"),
# # #         ("s", "push_screen('stats')", "Stats"),
# # #         ("h", "push_screen('head2head')", "Head 2 Head"),  # ,
# # #     ]

# # #     def __init__(self, df, path, start, end, all_time):
# # #         """Initialise df with data."""
# # #         self.df = df
# # #         self.path = path
# # #         self.start = start
# # #         self.end = end
# # #         self.all_time = all_time
# # #         super().__init__()

# # #     def compose(self) -> ComposeResult:
# # #         """."""
# # #         yield Static(
# # #             "[bold cyan]Welcome to my Football Application![/bold cyan]", id="footy_title"
# # #         )
# # #         yield Grid(
# # #             Button("Standings", id="standings"),
# # #             Button("Stats", id="stats"),
# # #             Button("H2H", id="h2h"),
# # #             Button("Quit", id="quit"),
# # #             id="homer",
# # #         )
# # #         yield Footer()

# # #     def on_mount(self) -> None:
# # #         """."""
# # #         self.install_screen(HomeScreen(), name="home")
# # #         self.install_screen(
# # #             Standings(self.df, self.path, self.start, self.end, self.all_time),
# # #             name="standings",
# # #         )
# # #         self.install_screen(StatsPage(), name="stats")
# # #         self.install_screen(Head2HeadPage(), name="head2head")

# # #     def on_button_pressed(self, event: Button.Pressed) -> None:
# # #         """."""
# # #         if event.button.id == "standings":
# # #             self.push_screen(
# # #                 Standings(self.df, self.path, self.start, self.end, self.all_time)
# # #             )
# # #         elif event.button.id == "stats":
# # #             self.push_screen(StatsPage())
# # #         elif event.button.id == "h2h":
# # #             self.push_screen(Head2HeadPage())
# # #         elif event.button.id == "quit":
# # #             self.push_screen(QuitScreen())


# # # class FootballApp(App):
# # #     """Run the app."""

# # #     CSS_PATH = "styling.tcss"

# # #     def __init__(self, df, path, start, end, all_time):
# # #         """Initialise df with data."""
# # #         self.df = df
# # #         self.path = path
# # #         self.start = start
# # #         self.end = end
# # #         self.all_time = all_time

# # #         super().__init__()

# # #     def compose(self) -> ComposeResult:
# # #         """Generate content."""
# # #         yield Header(name="Football Tables")
# # #         yield Label("Version", classes="version_label")
# # #         yield Digits(__version__, id="version_value")

# # #         with Horizontal(classes="table_container") as right:
# # #             dataframe = FootballDataTable(classes="table")
# # #             dataframe.border_title = "Table"
# # #             right.border_title = f"{self.path.replace('_', ' ')} {self.start}-{self.end}"
# # #             yield dataframe
# # #             with VerticalScroll(classes="inner_container") as inner:
# # #                 self.wicked_wango = Static("")
# # #                 inner.border_title = "Results"
# # #                 yield self.wicked_wango

# # #         yield Footer()

# # #     def on_mount(self):
# # #         """Add df when starting up."""
# # #         table = self.query_one(FootballDataTable)
# # #         table.add_df(self.df)

# # #     @on(FootballDataTable.CellHighlighted)
# # #     async def on_cell(self, event: FootballDataTable.CellHighlighted):
# # #         """Update results on cell hihglight."""
# # #         datapoint = str(event.value)

# # #         if "(C)" in datapoint or "(R)" in datapoint:
# # #             datapoint = datapoint.split("(")[0].strip()

# # #         magic_val = 3

# # #         if not self.all_time:
# # #             try:
# # #                 data = read_results(datapoint, self.path, self.start, self.end)
# # #             except FileNotFoundError as e:
# # #                 print(e)

# # #             if len(datapoint) > magic_val:
# # #                 data = read_results(datapoint, self.path, self.start, self.end)
# # #             else:
# # #                 data = ""
# # #         else:
# # #             data = "Can get results with: \
# # #                   \n\n`football get_game league season_start season_end`"

# # #         self.wicked_wango.update(data)


# # # class Standings(Screen):
# # #     """."""

# # #     def __init__(self, df, path, start, end, all_time):
# # #         """Initialise df with data."""
# # #         self.df = df
# # #         self.path = path
# # #         self.start = start
# # #         self.end = end
# # #         self.all_time = all_time
# # #         super().__init__()

# # #     def compose(self) -> ComposeResult:
# # #         """Generate content."""
# # #         yield Header(name="Football Tables")
# # #         yield Label("Version", classes="version_label")
# # #         yield Digits(__version__, id="version_value")

# # #         with Horizontal(classes="table_container") as right:
# # #             dataframe = FootballDataTable(classes="table")
# # #             dataframe.border_title = "Table"
# # #             right.border_title = f"{self.path.replace('_', ' ')} {self.start}-{self.end}"
# # #             yield dataframe
# # #             with VerticalScroll(classes="inner_container") as inner:
# # #                 self.wicked_wango = Static("")
# # #                 inner.border_title = "Results"
# # #                 yield self.wicked_wango

# # #         yield Button("Take me back", id="meny")
# # #         yield Footer()

# # #     def _on_mount(self) -> None:
# # #         table = self.query_one(FootballDataTable)
# # #         table.add_df(self.df)

# # #     def on_button_pressed(self, event: Button.Pressed) -> None:
# # #         """."""
# # #         if event.button.id == "meny":
# # #             self.dismiss(True)

# # #     @on(FootballDataTable.CellHighlighted)
# # #     async def on_cell(self, event: FootballDataTable.CellHighlighted) -> None:
# # #         """Update results on cell highlight."""
# # #         datapoint = str(event.value)

# # #         if "(C)" in datapoint or "(R)" in datapoint:
# # #             datapoint = datapoint.split("(")[0].strip()

# # #         magic_val = 3

# # #         if not self.all_time:
# # #             try:
# # #                 data = read_results(datapoint, self.path, self.start, self.end)
# # #             except FileNotFoundError as e:
# # #                 console.print(
# # #                     "[bold red]No results![/bold red]\
# # #                         [bold green]Use get_game[/bold green]",
# # #                     e,
# # #                 )

# # #             if len(datapoint) > magic_val:
# # #                 data = read_results(datapoint, self.path, self.start, self.end)
# # #             else:
# # #                 data = ""
# # #         else:
# # #             data = "Can get results with: \
# # #                   \n\n`football get_game league season_start season_end`"

# # #         self.wicked_wango.update(data)


# # # class StatsPage(Screen):
# # #     """."""

# # #     dff = DataFrame({"A": [1, 2, 3], "B": [34, 34, 456]})

# # #     def compose(self) -> ComposeResult:
# # #         """."""
# # #         with Horizontal(classes="inner_container") as outer:
# # #             outer.border_title = "basic stats"
# # #             df1 = Pretty(self.dff)
# # #             yield df1
# # #         yield Button("Take me back", id="back")
# # #         yield Footer()

# # #     def on_button_pressed(self, event: Button.Pressed):
# # #         """."""
# # #         if event.button.id == "back":
# # #             self.dismiss(True)


# # # class Head2HeadPage(Screen):
# # #     """."""

# # #     def __init__(self):
# # #         """."""
# # #         self.doop = Static("", id="button1", classes="team1")
# # #         self.beep = Static("", id="button2", classes="team2")
# # #         self.tits = RadioSet(*get_team_names(), id="button1")
# # #         self.tots = RadioSet(*get_team_names(), id="button2")
# # #         self.h2h_results = Static("")
# # #         self.h2h_stats = Static()
# # #         super().__init__()

# # #     def compose(self) -> ComposeResult:
# # #         """."""
# # #         yield Header(name="Welcome to Head 2 Head section", show_clock=True)
# # #         with Horizontal(classes="h2h_container") as outer:
# # #             outer.border_title = "Head 2 Head"

# # #             with VerticalScroll(classes="h2h") as team1:
# # #                 team1.border_title = "Team 1"
# # #                 yield self.tits

# # #             with Horizontal(classes="h2h") as h2h:
# # #                 h2h.border_title = "H2H"
# # #                 with Vertical(classes="team1"):
# # #                     yield self.doop
# # #                 with Vertical(classes="team2"):
# # #                     yield self.beep

# # #             with VerticalScroll(classes="h2h") as team2:
# # #                 team2.border_title = "Team 2"
# # #                 yield self.tots

# # #         with Horizontal(classes="statistics_container"):
# # #             with Vertical(classes="base_stats") as wang1:
# # #                 wang1.border_title = "Results"
# # #                 yield self.h2h_results
# # #             with Vertical(classes="base_stats") as wang:
# # #                 wang.border_title = "Stats"
# # #                 yield self.h2h_stats
# # #             with Vertical(classes="base_stats") as wong:
# # #                 wong.border_title = "Teams"

# # #                 yield Pretty(
# # #                     "Maybe add filters here for season if main screen just chooses league"
# # #                 )
# # #         yield Button("Take me Back", id="back")
# # #         yield Footer()

# # #     def on_mount(self):
# # #         """."""
# # #         self.team1 = None
# # #         self.team2 = None

# # #     def on_button_pressed(self, event: Button.Pressed):
# # #         """."""
# # #         if event.button.id == "back":
# # #             self.dismiss(True)

# # #     def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
# # #         """."""
# # #         if event.radio_set.id == "button1":
# # #             self.team1 = event.pressed.label
# # #             self.query_one("#button1", Static).update(self.team1)
# # #         if event.radio_set.id == "button2":
# # #             self.team2 = event.pressed.label
# # #             self.query_one("#button2", Static).update(self.team2)

# # #         if self.team1 and self.team2:
# # #             self.h2h_results.update(h2h_datatable(str(self.team1), str(self.team2)))
# # #             self.h2h_stats.update(more_deets(str(self.team1), str(self.team2)))


# # # class QuitScreen(Screen):
# # #     def compose(self) -> ComposeResult:
# # #         yield Grid(
# # #             Label("Are you sure?", id="question"),
# # #             Button("Yes", variant="error", id="yes"),
# # #             Button("No", variant="primary", id="no"),
# # #             id="quit_dialog",
# # #         )

# # #     def on_button_pressed(self, event:Button.Pressed) -> None:
# # #         if event.button.id == "yes":
# # #             self.app.exit()
# # #         else:
# # #             self.dismiss(False)

# # # class HomeScreen(Screen):
# # #     """."""

# # #     def __init__(self):
# # #         """."""
# # #         super().__init__()

# # #     def compose(self) -> ComposeResult:
# # #         """."""
# # #         yield Header(name="Barry")
# # #         yield Button("Standings", id="standings")
# # #         yield Button("Stats", id="stats")
# # #         yield Button("H2H", id="h2h")
# # #         yield Button("Quit", id="quit")
# # #         yield Footer()

# # #     def on_button_pressed(self, event: Button.Pressed):
# # #         """."""
# # #         if event.button.id == "standings":
# # #             self.dismiss(True)
# # #         elif event.button.id == "stats":
# # #             self.dismiss(True)
# # #         elif event.button.id == "h2h":
# # #             self.dismiss(True)
# # #         elif event.button.id == "quit":
# # #             self.dismiss(True)
# # # from textual.app import App, ComposeResult  # noqa: D100
# # # from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
# # # from textual.screen import Screen
# # # from textual.widgets import Button, Footer, Header, RadioSet, Static, Pretty

# # # from football.helper_functions import (
# # #     generic_read,
# # #     get_team_names,
# # #     h2h_datatable,
# # #     more_deets,
# # #     quick_read,
# # #     read_files,
# # #     read_seasons,
# # #     season_data,
# # # )
# # # from football.tui.the_table import FootballDataTable


# # # def _me_rule():
# # #     return lambda row: sum(map(int, re.findall(r"(\d+|\-\d+)", row)))
# # """Manchester United
# # 1
# # 42
# # 24
# # 12
# # 6
# # 67
# # 31
# # 36
# # 84
# # Aston Villa
# # 2
# # 42
# # 21
# # 11
# # 10
# # 57
# # 40
# # 17
# # 74
# # Norwich City
# # 3
# # 42
# # 21
# # 9
# # 12
# # 61
# # 65
# # -4
# # 72
# # Blackburn Rovers
# # 4
# # 42
# # 20
# # 11
# # 11
# # 68
# # 46
# # 22
# # 71
# # Queens Park Rangers
# # 5
# # 42
# # 17
# # 12
# # 13
# # 63
# # 55
# # 8
# # 63
# # Liverpool
# # 6
# # 42
# # 16
# # 11
# # 15
# # 62
# # 55
# # 7
# # 59
# # Sheffield Wednesday
# # 7
# # 42
# # 15
# # 14
# # 13
# # 55
# # 51
# # 4
# # 59
# # Tottenham Hotspur
# # 8
# # 42
# # 16
# # 11
# # 15
# # 60
# # 66
# # -6
# # 59
# # Manchester City
# # 9
# # 42
# # 15
# # 12
# # 15
# # 56
# # 51
# # 5
# # 57
# # Arsenal
# # 10
# # 42
# # 15
# # 11
# # 16
# # 40
# # 38
# # 2
# # 56
# # Chelsea
# # 11
# # 42
# # 14
# # 14
# # 14
# # 51
# # 54
# # -3
# # 56
# # Wimbledon
# # 12
# # 42
# # 14
# # 12
# # 16
# # 56
# # 55
# # 1
# # 54
# # Everton
# # 13
# # 42
# # 15
# # 8
# # 19
# # 53
# # 55
# # -2
# # 53
# # Sheffield United
# # 14
# # 42
# # 14
# # 10
# # 18
# # 54
# # 53
# # 1
# # 52
# # Coventry City
# # 15
# # 42
# # 13
# # 13
# # 16
# # 52
# # 57
# # -5
# # 52
# # Ipswich Town
# # 16
# # 42
# # 12
# # 16
# # 14
# # 50
# # 55
# # -5
# # 52
# # Leeds United
# # 17
# # 42
# # 12
# # 15
# # 15
# # 57
# # 62
# # -5
# # 51
# # Southampton
# # 18
# # 42
# # 13
# # 11
# # 18
# # 54
# # 61
# # -7
# # 50
# # Oldham Athletic
# # 19
# # 42
# # 13
# # 10
# # 19
# # 63
# # 74
# # -11
# # 49
# # Crystal Palace
# # 20
# # 42
# # 11
# # 16
# # 15
# # 48
# # 61
# # -13
# # 49
# # Middlesbrough
# # 21
# # 42
# # 11
# # 11
# # 20
# # 54
# # 75
# # -21
# # 44
# # Nottingham Forest
# # 22
# # 42
# # 10
# # 10
# # 22
# # 41
# # 62
# # -21
# # 40
# # """

# # expected_data = {
# #     "Team": [
# #         "Manchester United",
# #         "Aston Villa",
# #         "Norwich City",
# #         "Blackburn Rovers",
# #         "Queens Park Rangers",
# #         "Liverpool",
# #         "Sheffield Wednesday",
# #         "Tottenham Hotspur"
# #         "Manchester City"
# #         "Arsenal"
# #         "Chelsea"
# #         "Wimbledon"
# #         "Everton"
# #         "Sheffield United"
# #         "Coventry City"
# #         "Ipswich Town"
# #         "Leeds United"
# #         "Southampton"
# #         "Oldham Athletic"
# #         "Crystal Palace"
# #         "Middlesbrough"
# #         "Nottingham Forest",
# #     ],
# #     "Pos": [
# #         "1",
# #         "2",
# #         "3",
# #         "4",
# #         "5",
# #         "6",
# #         "7",
# #         "8",
# #         "9",
# #         "10",
# #         "11",
# #         "12",
# #         "13",
# #         "14",
# #         "15",
# #         "16",
# #         "17",
# #         "18",
# #         "19",
# #         "20",
# #         "21",
# #         "22",
# #     ],
# #     "Pld": [
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #         "42",
# #     ],
# #     "W": [
# #         "24",
# #         "21",
# #         "21",
# #         "20",
# #         "17",
# #         "16",
# #         "15",
# #         "16",
# #         "15",
# #         "15",
# #         "14",
# #         "14",
# #         "15",
# #         "14",
# #         "13",
# #         "12",
# #         "12",
# #         "13",
# #         "13",
# #         "11",
# #         "11",
# #         "10",
# #     ],
# #     "D": [
# #         "12",
# #         "11",
# #         "9",
# #         "11",
# #         "12",
# #         "11",
# #         "14",
# #         "11",
# #         "12",
# #         "11",
# #         "14",
# #         "12",
# #         "8",
# #         "10",
# #         "13",
# #         "16",
# #         "15",
# #         "11",
# #         "10",
# #         "16",
# #         "11",
# #         "10",
# #     ],
# #     "L": [
# #         "6",
# #         "10",
# #         "12",
# #         "11",
# #         "13",
# #         "15",
# #         "13",
# #         "15",
# #         "15",
# #         "16",
# #         "14",
# #         "16",
# #         "19",
# #         "18",
# #         "16",
# #         "14",
# #         "15",
# #         "18",
# #         "19",
# #         "15",
# #         "20",
# #         "22",
# #     ],
# #     "GF": [
# #         "67",
# #         "57",
# #         "61",
# #         "68",
# #         "63",
# #         "62",
# #         "55",
# #         "60",
# #         "56",
# #         "40",
# #         "51",
# #         "56",
# #         "53",
# #         "54",
# #         "52",
# #         "50",
# #         "57",
# #         "54",
# #         "63",
# #         "48",
# #         "54",
# #         "41",
# #     ],
# #     "GA": [
# #         "31",
# #         "40",
# #         "65",
# #         "46",
# #         "55",
# #         "55",
# #         "51",
# #         "66",
# #         "51",
# #         "38",
# #         "54",
# #         "55",
# #         "55",
# #         "53",
# #         "57",
# #         "55",
# #         "62",
# #         "61",
# #         "74",
# #         "61",
# #         "75",
# #         "62",
# #     ],
# #     "GD": [
# #         "36",
# #         "17",
# #         "-4",
# #         "22",
# #         "8",
# #         "7",
# #         "4",
# #         "-6",
# #         "5",
# #         "2",
# #         "-3",
# #         "1",
# #         "-2",
# #         "1",
# #         "-5",
# #         "-5",
# #         "-5",
# #         "-7",
# #         "-11",
# #         "-13",
# #         "-21",
# #         "-21",
# #     ],
# #     "Pts": [
# #         "84",
# #         "74",
# #         "72",
# #         "71",
# #         "63",
# #         "59",
# #         "59",
# #         "59",
# #         "57",
# #         "56",
# #         "56",
# #         "54",
# #         "53",
# #         "52",
# #         "52",
# #         "52",
# #         "51",
# #         "50",
# #         "49",
# #         "49",
# #         "44",
# #         "40",
# #     ],
# # }


# def txt_to_df(
#     league: str,
#     start: str,
#     end: str,
# ) -> DataFrame:
#     """Convert a standardized txt file into a DataFrame.

#     Args:
#     ----
#         league (league): A string given from command line to insert into file to read.
#         start (start): A string given from command line to insert into file
#           to read.
#         end (end): A string given from command line to insert into file
#         to read.

#     Returns:
#     -------
#         Table: A Pandas DataFrame.

#     """
#     path = Path.cwd() / "refined_data" / league / f"{start}_{end}.txt"
#     try:
#         with open(path) as f:
#             lines = f.readlines()
#     except FileNotFoundError as e:
#         console.print(
#             """[bold magenta3]File does not exist bellend[/bold magenta3]\n\
# [bold green]Try get command first[/bold green]""",
#             e,
#         )
#         raise SystemExit(1) from e

#     table = [lines[x : x + 10] for x in range(0, len(lines), 10)]
#     table = [[i.strip() for i in j] for j in table]

#     table1 = []
#     for i in table:
#         tmp = i[1]
#         i[1] = i[0]
#         i[0] = tmp
#         table1.append(i)

#     cols = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]

#     return DataFrame(table1, columns=cols)
