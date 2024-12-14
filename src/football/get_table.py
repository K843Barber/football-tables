import requests  # noqa: D100
from bs4 import BeautifulSoup
from pandas import DataFrame


def get_table(
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
    keyword1 = [
        "Qualification",
        "Relegation",
        "Serie ",
        "Champions ",
        "Europa ",
        "Excluded",
        "Intertoto",
        "UEFA",
    ]

    if league != "Allsvenskan":
        url = (
            f"https://en.wikipedia.org/wiki/{season_start}%E2%80%93{season_end}_{league}"
        )
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

    with open(f"data/{league}-{season_start}-{season_end}.txt", "w") as f:
        for i in table[10:]:
            f.writelines(f"{i}\n")


def get_game_results(league: str, season_start: str, season_end: str) -> None:
    """Get league results for all teams."""
    url = f"https://en.wikipedia.org/wiki/{season_start}%E2%80%93{season_end}_{league}"

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
    df.to_csv(f"data/{league}_{season_start}_{season_end}_results.csv", index=False)
