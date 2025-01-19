"""Fetch league details."""

from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def get_table(league: str, start: str, end: str) -> None:
    """Needed to extract a season table from top five leagues.

    Args:
    ----
        league: The league you require (PL, Bundesliga, La Liga, Ligue1, SerieA).
        start: The year the beginning of the season occurs.
        end: The year the end of the season occurs.

    """
    if league != "Allsvenskan":
        if start not in ("1899", "1999"):
            url = f"https://en.wikipedia.org/wiki/{start}%E2%80%93{end[2:]}_{league}"
        else:
            url = f"https://en.wikipedia.org/wiki/{start}%E2%80%93{end}_{league}"
    else:
        url = f"https://en.wikipedia.org/wiki/{start}_{league}"

    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.text, "html.parser")
    try:
        tabs = soup.find("table", {"class": "wikitable", "style": "text-align:center;"})
    except TypeError:
        return None

    table: list = []

    rows = tabs.find_all("tr")
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


def get_very_specific_table(league: str, start: str, end: str) -> None:
    """Needed to extract a season table from top five leagues.

    Args:
    ----
        league: The league you require (PL, Bundesliga, La Liga, Ligue1, SerieA).
        start: The year the beginning of the season occurs.
        end: The year the end of the season occurs.

    """
    url = f"https://en.wikipedia.org/wiki/{start}_{league}"

    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.text, "html.parser")
    try:
        tabs = soup.find("table", {"class": "wikitable", "style": "text-align:center;"})
    except TypeError:
        return None

    table: list = []

    rows = tabs.find_all("tr")
    for row in rows:
        for cell in row.find_all("th"):
            if cell.text.strip() != "":
                table.append(cell.text.strip())

        for cell in row.find_all("td"):
            if cell.text.strip() != "":
                table.append(cell.text.strip())

    path = Path.cwd() / "data" / league
    path.mkdir(parents=True, exist_ok=True)
    filepath = path / f"{int(start) - 1}_{int(end) - 1}.txt"

    with filepath.open("w", encoding="utf-8") as f:
        for i in table[10:]:
            f.writelines(f"{i}\n")


def get_very_specific_game_results(league: str, start: str, end: str) -> None:
    """Get league results for all teams."""
    url = f"https://en.wikipedia.org/wiki/{start}_{league}"

    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.text, "html.parser")
    tabs = soup.find(
        "table",
        {
            "class": "wikitable plainrowheaders",
            "style": "text-align:center;font-size:100%;",
        },
    )

    lookup_table: dict = {}
    season_results: list = []

    rows = tabs.find_all("tr")
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

    path = Path.cwd() / "data" / league / f"{int(start) - 1}_{int(end) - 1}_results.csv"
    df.to_csv(path, index=False)


def get_game_results(league: str, start: str, end: str) -> None:
    """Get league results for all teams."""
    if league != "Allsvenskan":
        if start not in ("1899", "1999"):
            url = f"https://en.wikipedia.org/wiki/{start}%E2%80%93{end[2:]}_{league}"
        else:
            url = f"https://en.wikipedia.org/wiki/{start}%E2%80%93{end}_{league}"
    else:
        url = f"https://en.wikipedia.org/wiki/{start}_{league}"

    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.text, "html.parser")
    tabs = soup.find(
        "table",
        {
            "class": "wikitable plainrowheaders",
            "style": "text-align:center;font-size:100%;",
        },
    )

    lookup_table: dict = {}
    season_results: list = []

    rows = tabs.find_all("tr")
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


def get_specific_season(league: str, begin: str, end: str):
    """."""
    from rich.console import Console

    console = Console()

    with console.status("[bold magenta]Fetching[/bold magenta]"):
        get_very_specific_table(league, begin, end)
        sleep(0.1)
        get_very_specific_game_results(league, begin, end)
        sleep(0.1)


def get_season(league: str, begin: str, end: str):
    """."""
    from rich.console import Console

    console = Console()

    with console.status("[bold magenta]Fetching[/bold magenta]"):
        get_table(league, begin, end)
        sleep(0.1)
        get_game_results(league, begin, end)
        sleep(0.1)


def get_alot(league: str, begin: str, end: str):
    """."""
    progress_bar = Progress(
        SpinnerColumn(),
        TextColumn(
            "[bold cyan]Fetching[/bold cyan][progress.percentage]{task.percentage:>3.0f}%"
        ),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
    )

    with progress_bar as p:
        for num in p.track(range(int(begin), int(end) - 1, 1)):
            get_table(league, str(num), str(num + 1))
            sleep(0.1)
            get_game_results(league, str(num), str(num + 1))
            sleep(0.1)
