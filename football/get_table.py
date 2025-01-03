from pathlib import Path  # noqa: D100
from time import sleep

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Column


def get_table(  # noqa: C901
    league: str,
    season_start: str,
    season_end: str,
) -> None:
    """Needed to extract a season table from top five leagues.

    Args:
    ----
        league: The league you require (PL, Bundesliga, La Liga, Ligue1, SerieA).
        season_start: The year the beginning of the season occurs.
        season_end: The year the end of the season occurs.

    """

    def _grab_leagues():  # noqa: C901
        """."""
        keyword1 = [  # Make this better by ignoring this and fixing in the clean
            "Qualification",
            "Relegation",
            "Serie ",
            "Champions ",
            "Europa ",
            "Excluded",
            "Intertoto",
            "UEFA",
            "Banned",
            "Not admitted",
            "Qualified",
            "Invited",
            "Latin Cup",
            # "[1]",
            "Chosen",
            # "[a]",
            # "[b]",
        ]
        if league != "Allsvenskan":
            if season_start != "1999":
                url = f"https://en.wikipedia.org/wiki/{season_start}%E2%80%93{season_end[2:]}_{league}"
            else:
                url = f"https://en.wikipedia.org/wiki/{season_start}%E2%80%93{season_end}_{league}"
        else:
            url = f"https://en.wikipedia.org/wiki/{season_start}_{league}"

        page = requests.get(url)  # noqa: S113
        soup = BeautifulSoup(page.text, "html.parser")
        tabs = soup.find("table", {"class": "wikitable", "style": "text-align:center;"})
        rows = tabs.find_all("tr")

        table = []

        for row in rows:
            for cell in row.find_all("th"):
                if all(string not in cell.text for string in keyword1):
                    if cell.text.strip() != "":
                        table.append(cell.text.strip())

            for cell in row.find_all("td"):
                if all(string not in cell.text for string in keyword1):
                    if cell.text.strip() != "":
                        table.append(cell.text.strip())

        path = Path.cwd() / "data" / league
        path.mkdir(parents=True, exist_ok=True)
        filepath = path / f"{season_start}_{season_end}.txt"

        with filepath.open("w") as f:
            for i in table[10:]:
                f.writelines(f"{i}\n")

    _grab_leagues()


def get_game_results(league: str, season_start: str, season_end: str) -> None:
    """Get league results for all teams."""

    def _grab_results():
        if league != "Allsvenskan":
            if season_start != "1999":
                url = f"https://en.wikipedia.org/wiki/{season_start}%E2%80%93{season_end[2:]}_{league}"
            else:
                url = f"https://en.wikipedia.org/wiki/{season_start}%E2%80%93{season_end}_{league}"
        else:
            url = f"https://en.wikipedia.org/wiki/{season_start}_{league}"

        page = requests.get(url)  # noqa: S113
        soup = BeautifulSoup(page.text, "html.parser")
        tabs = soup.find(
            "table",
            {
                "class": "wikitable plainrowheaders",
                "style": "text-align:center;font-size:100%;",
            },
        )

        rows = tabs.find_all("tr")

        lookup_table: dict = {}
        season_results = []
        for en, row in enumerate(rows):
            for cell in row.find_all("th"):
                if en == 0:
                    continue
                if cell.text.strip("\n") not in lookup_table:
                    lookup_table[en] = cell.text.strip("\n")

        for home, row in enumerate(rows):
            for away, cell in enumerate(row.find_all("td"), start=1):
                h, a = lookup_table[home], lookup_table[away]
                res = cell.text.strip("\n")
                season_results.append((h, res, a))

        df = DataFrame(season_results, columns=["Home", "Result", "Away"])

        df = df[df["Home"] != df["Away"]]
        df = df[df["Result"] != ""]
        df = df[df["Result"] != "a"]
        return df

    df = _grab_results()

    path = Path.cwd() / "data" / league / f"{season_start}_{season_end}_results.csv"
    df.to_csv(path, index=False)


def get_alot(league: str, begin: str, end: str):
    """."""
    text_column = TextColumn("{task.description}", table_column=Column(ratio=1))
    bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
    progress = Progress(text_column, bar_column, expand=True)

    with progress:
        for num in progress.track(
            range(int(begin), int(end) - 1, 1),
            description="[bold magenta]Fetching[/bold magenta]",
        ):
            get_table(league, str(num), str(num + 1))
            sleep(0.1)
            get_game_results(league, str(num), str(num + 1))
            sleep(0.1)
