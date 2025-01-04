"""Functions to clean the data."""

from pathlib import Path

from numpy import reshape
from pandas import DataFrame, read_csv, to_numeric
from rich.progress import track


def stripping(strings: str):
    """."""
    skip_type1 = [
        "[b]",
        "[a]",
        "[c]",
        "[d]",
        "[e]",
        "[g]",
        "[f]",
        "[1]",
        "[h]",
        "[i]",
        "[j]",
    ]
    skip_type2 = [
        "Cup Winners' Cup",
        "Mitropa",
        "Segunda",
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
        "Chosen",
    ]
    if " (" in strings:
        strings = strings.split(" (")[0]
    for ext in skip_type1:
        if ext in strings:
            strings = strings.split("[")[0]

    for ext in skip_type2:
        if ext in strings:
            strings = ""

    return strings.strip("\n").strip().replace("\xa0", " ")


def correct_names(strings: str):
    """."""
    fixit: dict = {
        "Milan": "AC Milan",
        "Inter Milan": "Internazionale",
        "Inter": "Internazionale",
        "ChievoVerona": "Chievo",
        "Paris SG": "Paris Saint-Germain",
        "Deportivo de La Coruña": "Deportivo La Coruña",
        "FC Barcelona": "Barcelona",
        "CF Barcelona": "Barcelona",
        "Valencia CF": "Valencia",
        "Hércules CF": "Hércules",
        "Racing de Santander": "Racing Santander",
        "Celta de Vigo": "Celta Vigo",
        "CD Tenerife": "Tenerife",
        "Sevilla FC": "Sevilla",
        "UD Salamanca": "Salamanca",
        "RCD Espanyol": "Espanyol",
        "SD Compostela": "Compostela",
        "Sporting de Gijón": "Sporting Gijón",
        "CF Extramadura": "Extramadura",
        "CP Mérida": "Mérida",
        "CD Logroñés": "Logroñés",
        "AD Almería": "Almería",
        "Alavés": "Deportivo Alavés",
        "Albacete Balompié": "Albacete",
        "Atlético Bilbao": "Athletic Bilbao",
        "Betis": "Real Betis",
        "CD Castellón": "Castellón",
        "CD Málaga": "Málaga",
        "CE Sabadell FC": "Sabadell",
        "CF Extremadura": "Extremadura",
        "Celta": "Celta Vigo",
        "Cádiz CF": "Cádiz",
        "Córdoba CF": "Córdoba",
        "Elche CF": "Elche",
        "Granada CF": "Granada",
        "La Coruña": "Deportivo La Coruña",
        "Pontevedra CF": "Pontevedra",
        "RCD Español": "Español",
        "RCD Mallorca": "Mallorca",
        "Recreativo": "Recreativo de Huelva",
        "Sevilla CF": "Sevilla",
        "UD Las Palmas": "Las Palmas",
    }
    if strings in fixit:
        return fixit[strings]
    else:
        return strings


def fix_gd(problem_list: list) -> list:
    """."""
    for i in range(8, len(problem_list), 10):
        problem_list[i] = int(problem_list[i - 2]) - int(problem_list[i - 1])

    return problem_list


def clean_it(league: str):
    """."""
    path = Path.cwd() / "data" / league
    files = path.rglob("*.txt")

    for file in sorted(files):
        rewritten_file = []
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                ll = stripping(line)
                lll = correct_names(ll)
                if lll != "":
                    rewritten_file.append(lll)
        rewritten_file = fix_gd(rewritten_file)
        new_path = Path.cwd() / "refined_data" / league

        new_path.mkdir(parents=True, exist_ok=True)
        filepath = new_path / file.name

        with open(filepath, "w") as f:
            for item in rewritten_file:
                f.writelines(f"{item}\n")


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
    path = Path.cwd() / "data" / league
    files = path.rglob("*results.csv")
    for file in track(files, description="[bold green]Cleaning...[/bold green]"):
        tmp_df = fix_dataframe(file)

        corrected_file = []
        holder = file.stem.split("_r")[0].split("_")[0]

        for row in tmp_df.values:
            if holder == "1979" and "CD Málaga" in row and "UD Salamanca" in row:
                for cell in ["CD Málaga", "0", "3", "UD Salamanca"]:
                    corrected_file.append(cell)
            else:
                for cell in row:
                    val = stripping(cell)
                    val = correct_names(val)
                    corrected_file.append(val)
        new_file = DataFrame(reshape(corrected_file, (int(len(corrected_file) / 4), 4)))
        new_file.columns = ["Home", "HS", "AS", "Away"]

        new_file["AS"] = to_numeric(new_file["AS"])
        new_path = Path.cwd() / "refined_data" / league
        new_path.mkdir(parents=True, exist_ok=True)
        filepath = new_path / file.name
        new_file.to_csv(filepath, sep=",", index=False)


# clean_that("La_Liga")
# clean_it("Bundesliga")
