"""Functions to clean the data."""

from pathlib import Path

from numpy import reshape
from pandas import DataFrame, read_csv
from rich.progress import track

from football.common.clean_me_helper import list_a, list_b, lookup_table


# --------------------- Strip the data ---------------------
def table_stripping(strings: str) -> str:
    """."""
    skip_type1 = list_a
    skip_type2 = list_b

    if strings is not None:
        if " (" in strings:
            strings = strings.split(" (")[0]
        for ext in skip_type1:
            if ext in strings:
                strings = strings.split("[")[0]

        for ext in skip_type2:
            if ext in strings:
                strings = ""
        return strings.strip("\n").strip().replace("\xa0", " ")


def results_stripping(strings: str) -> str:
    """."""
    skip_type1 = list_a
    skip_type2 = list_b

    if strings is not None:
        strings = strings.strip(")").strip("(")
        for ext in skip_type1:
            if ext in strings:
                strings = strings.split("[")[0]

        for ext in skip_type2:
            if ext in strings:
                strings = ""
        if strings == "1b":
            strings = strings[0]
        return strings.strip("\n").strip().replace("\xa0", " ")


def correct_names(strings: str):
    """."""
    fixit = lookup_table
    if strings in fixit:
        return fixit[strings]
    else:
        return strings


# --------------------- Convert the data ---------------------
def fix_gd(problem_list: list) -> list:
    """."""
    for i in range(8, len(problem_list), 10):
        problem_list[i] = int(problem_list[i - 2]) - int(problem_list[i - 1])

    return problem_list


def combine_home_and_away(problem_list: list) -> list:
    """."""
    for j, i in enumerate(range(3, len(problem_list), 5)):
        if j % 3 == 0:
            problem_list[i] = int(problem_list[i]) + int(problem_list[i + 5])
            problem_list[i + 1] = int(problem_list[i + 1]) + int(problem_list[i + 6])
            problem_list[i + 2] = int(problem_list[i + 2]) + int(problem_list[i + 7])
            problem_list[i + 3] = int(problem_list[i + 3]) + int(problem_list[i + 8])
            problem_list[i + 4] = int(problem_list[i + 4]) + int(problem_list[i + 9])

    new_list = []
    for i in range(0, len(problem_list), 15):
        new_list.append(problem_list[i : i + 8])
        new_list.append([problem_list[i + 6] - problem_list[i + 7]])
        new_list.append([int(problem_list[i + 14])])

    new_list = [i for j in new_list for i in j]

    return new_list


# --------------------- Loop and tidy the data ---------------------
def clean_it(league: str):
    """."""
    path = Path.cwd() / "data/uncleansed" / league
    files = path.rglob("*.txt")

    for file in sorted(files):
        rewritten_file = []
        with open(file) as f:
            lines = f.readlines()
            if file.stem in ("1890_1891", "1891_1892"):
                lines = lines[5:]
                for line in lines:
                    ll = table_stripping(line)
                    lll = correct_names(ll)
                    if lll != "":
                        rewritten_file.append(lll)
                rewritten_file = combine_home_and_away(rewritten_file)
            elif league == "Ligue_1" and file.stem == "2019_2020":
                for line in lines:
                    ll = table_stripping(line)
                    lll = correct_names(ll)
                    if lll != "":
                        rewritten_file.append(lll)
                del rewritten_file[10::11]
            else:
                for line in lines:
                    ll = table_stripping(line)
                    lll = correct_names(ll)
                    if lll != "":
                        rewritten_file.append(lll)
                rewritten_file = fix_gd(rewritten_file)

        # --------------------- Write the data ---------------------
        # --------------------- Should separate ---------------------
        if league == "Football_League_First_Division":
            new_path = Path.cwd() / "data/leagues" / "Premier_League"
        else:
            new_path = Path.cwd() / "data/leagues" / league

        new_path.mkdir(parents=True, exist_ok=True)
        filepath = new_path / file.name

        with open(filepath, "w", encoding="utf-8") as f:
            for item in rewritten_file:
                f.writelines(f"{item}\n")


# --------------------- Section refers to results ---------------------
def fix_dataframe(file: Path) -> DataFrame:
    """."""
    tmp_df = DataFrame(read_csv(file))
    tmp_df["Home"] = tmp_df["Home"].str.replace(" ", " ")  # noqa: RUF001
    tmp_df["Away"] = tmp_df["Away"].str.replace(" ", " ")  # noqa: RUF001
    tmp_df["Home"] = tmp_df["Home"].str.replace("\xa0", " ")
    tmp_df["Away"] = tmp_df["Away"].str.replace("\xa0", " ")

    tmp_df["Result"] = tmp_df["Result"].str.replace("−", "–")  # noqa: RUF001
    tmp_df[["HS", "AS"]] = tmp_df["Result"].str.split("–", expand=True)  # noqa: RUF001
    tmp_df = tmp_df.drop(["Result"], axis=1)
    tmp_df = tmp_df[["Home", "HS", "AS", "Away"]]
    return tmp_df


def clean_that(league: str):
    """."""
    path = Path.cwd() / "data/uncleansed" / league
    files = path.rglob("*results.csv")
    for file in sorted(
        track(files, description=f"[bold green]Cleaning {league}...[/bold green]")
    ):
        tmp_df = fix_dataframe(file)
        corrected_file = []
        holder = file.stem.split("_r")[0].split("_")[0]

        for row in tmp_df.values:
            if holder == "1979" and "CD Málaga" in row and "UD Salamanca" in row:
                for cell in ["CD Málaga", "0", "3", "UD Salamanca"]:
                    corrected_file.append(cell)
            else:
                for cell in row:
                    val = results_stripping(cell)
                    val = correct_names(val)
                    if val != "":
                        corrected_file.append(val)

        new_file = DataFrame(reshape(corrected_file, (int(len(corrected_file) / 4), 4)))
        new_file = new_file.dropna()
        new_file.columns = ["Home", "HS", "AS", "Away"]

        for _, row in new_file.iterrows():
            if "-" in row["HS"]:
                row.iloc[1], row.iloc[2] = row["HS"].split("-")

        if league == "Football_League_First_Division":
            new_path = Path.cwd() / "data/leagues" / "Premier_League"
        else:
            new_path = Path.cwd() / "data/leagues" / league
        new_path.mkdir(parents=True, exist_ok=True)
        filepath = new_path / file.name
        new_file.to_csv(filepath, sep=",", index=False)


def rinse(league: str):
    """Dev to clean, not for general use, since all data should be cleaned."""
    clean_that(league)
    clean_it(league)
