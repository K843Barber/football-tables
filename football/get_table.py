"""Fetch league details."""

import logging
from multiprocessing import Pool
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from rich import print
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from football.common import clean_me
from football.common.config import load_config

log = logging.getLogger(__name__)

console = Console()


def _fetch_url(league: str, start: str, end: str):
    """."""
    if league != "Allsvenskan":
        if league == "La_Liga" and start == "1928" and end == "1929":
            url = f"https://en.wikipedia.org/wiki/{end}_{league}"
        else:  # noqa: PLR5501
            if start not in ("1899", "1999"):
                url = f"https://en.wikipedia.org/wiki/{start}%E2%80%93{end[2:]}_{league}"
            else:
                url = f"https://en.wikipedia.org/wiki/{start}%E2%80%93{end}_{league}"
    else:
        url = f"https://en.wikipedia.org/wiki/{start}_{league}"

    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        print(
            f"Season [bold cyan]{start}-{end[2:]}[/bold cyan] for \
[bold dark_orange]{league}[/bold dark_orange] \
[bold red]not found[/bold red]"
        )
        return

    return page


def _fetch_table(soup, league, start, end) -> None:
    tables = soup.find("table", {"class": "wikitable", "style": "text-align:center;"})
    table: list = []

    rows = tables.find_all("tr")
    for row in rows:
        for cell in row.find_all("th"):
            if cell.text.strip() != "":
                table.append(cell.text.strip())

        for cell in row.find_all("td"):
            if cell.text.strip() != "":
                table.append(cell.text.strip())

    path = Path.cwd() / "data" / league
    path.mkdir(parents=True, exist_ok=True)
    filepath = path / f"{start}_{end}.txt"

    with filepath.open("w", encoding="utf-8") as f:
        for i in table[10:]:
            f.writelines(f"{i}\n")


def _fetch_results(soup, league: str, start: str, end: str) -> None:
    """."""
    tables = soup.find(
        "table",
        {
            "class": "wikitable plainrowheaders",
            "style": "text-align:center;font-size:100%;",
        },
    )

    lookup_table: dict = {}
    season_results: list = []

    rows = tables.find_all("tr")
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

    path = Path.cwd() / "data" / league / f"{start}_{end}_results.csv"
    df.to_csv(path, index=False)


# --------------------------- Main table ---------------------------
def get_table(league: str, start: str, end: str) -> None:
    """Needed to extract a season table from top five leagues.

    Args:
    ----
        league: The league you require (PL, Bundesliga, La Liga, Ligue1, SerieA).
        start: The year the beginning of the season occurs.
        end: The year the end of the season occurs.
        advance: If no url, advance

    """
    page = _fetch_url(league, start, end)
    if page is not None:
        soup = BeautifulSoup(page.text, "html.parser")

        _fetch_table(soup, league, start, end)
        _fetch_results(soup, league, start, end)


# --------------------------- Combined season getters ---------------------------
def get_season(league: str, season: list):
    """Fetch both table and results."""
    with console.status(f"[bold magenta]Fetching {league} {season}[/bold magenta]"):
        get_table(league, *season)
        sleep(0.1)

    clean_me.clean_it(league)
    clean_me.clean_that(league)


def get_alot(league: str, season: list):
    """Fetch several seasons tables and results."""
    progress_bar = Progress(
        SpinnerColumn(),
        TextColumn(
            "[bold cyan]Fetching...[/bold cyan][progress.percentage]{task.percentage:>3.0f}%"  # noqa: E501
        ),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
    )

    with progress_bar as p:
        for num in p.track(range(int(season[0]), int(season[1]) - 1, 1)):
            get_table(league, str(num), str(num + 1))
            sleep(0.1)

    clean_me.clean_it(league)
    clean_me.clean_that(league)


def multi(league):
    """Use for updating leagues concurrently."""
    clean_me.clean_it(league)
    clean_me.clean_that(league)


def update_leagues():
    """Get leagues either from given arg or config."""
    leagues, season = load_config()

    for league in leagues:
        with console.status(f"[bold magenta]Fetching {league} {season}[/bold magenta]"):
            get_table(league, season, str(int(season) + 1))

    with Pool(processes=8) as pool:
        pool.map(multi, leagues)
