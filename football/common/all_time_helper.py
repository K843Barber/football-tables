import re  # noqa: D100
from pathlib import Path

from pandas import DataFrame, concat
from rich.table import Table

from football.common.format_tables import df_to_table, give_dataframe
from football.common.league_page_helper import read_seasons


def all_time_table(league: str, seasons: list) -> DataFrame:
    """Give DataFrame with all seasons."""
    cols = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    all_time = DataFrame(columns=cols)

    dfs = []
    for season in seasons:
        df = give_dataframe(league, f"{season}", f"{int(season) + 1}")

        df["Team"] = df["Team"].str.replace(r"\(.*\)", "", regex=True)
        df["Pts"] = df["Pts"].str.replace(r"\[.*\]", "", regex=True)
        df["Team"] = df["Team"].str.rstrip(" ")

        dfs.append(df)

    all_time = DataFrame(concat(dfs))
    columns = ["Pos", "Pts", "Pld", "W", "D", "L", "GF", "GA"]
    all_time[columns] = all_time[columns].astype(int)

    def _me_rule():
        return lambda row: sum(map(int, re.findall(r"(\d+|-\d+)", row)))

    # Ugly fixes here
    all_time["GD"] = all_time["GD"].apply(_me_rule())

    all_time["T1"] = all_time["Team"].str.split("[", expand=False)
    all_time["T1"] = all_time["T1"].str[0]
    all_time["Team"] = all_time["T1"]
    all_time = all_time.drop(columns=["T1"])

    new = all_time.groupby(by="Team", as_index=False).sum()
    df = DataFrame(new).sort_values("Pts", ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    df["Pos"] = df.index
    df[["Team", "Pos"]] = df[["Pos", "Team"]]

    return df


def get_smallest(league: str):
    """Grab the earliest season for the all time table."""
    return min([int(i.split("_")[0]) for i in read_seasons(league)])


def league_winners(league: str):
    """."""
    path = Path.cwd() / "refined_data" / league
    files = path.rglob("*.txt")

    titles: dict = {}

    for file in sorted(files)[:-1]:
        winner = file.read_text().split("\n")[0]
        if winner in titles:
            titles[winner] += 1
        else:
            titles[winner] = 1

    titles = dict(sorted(titles.items(), key=lambda item: item[1], reverse=True))
    titles_df = DataFrame(titles, index=["0"]).T
    titles_df["Team"] = titles_df.index
    titles_df.columns = ["Wins", "Team"]
    titles_df = titles_df[["Team", "Wins"]]
    table = Table(header_style="bold cyan", border_style="dim cyan")

    return df_to_table(titles_df, table)


# league_winners("Premier_League")
