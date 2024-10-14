import requests
from bs4 import BeautifulSoup


def get_table(
    league: str,
    season_start: str,
    season_end: str,
) -> None:
    """
    Needed to extract a season table from top five leagues.

    Args:
    ----
        league: The league you require (PL, Bundesliga, La Liga, Ligue1, SerieA).
        season_start: The year the beginning of the season occurs.
        season_end: The year the end of the season occurs.

    """
    keyword1 = ["Qualification", "Relegation", "Serie ", "Champions ", "Europa ", "Excluded", "Intertoto", "UEFA"]

    url = f"https://en.wikipedia.org/wiki/{season_start}%E2%80%93{season_end}_{league}"
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
