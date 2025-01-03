from pathlib import Path  # noqa: D100

from numpy import reshape
from pandas import DataFrame, read_csv, to_numeric
from rich.progress import track

# Use file to clean the scraped data
# Store problems with data here and look to align things and remove from codebase


# Issue with querying goals for/against in datatable page. Need to align csv
# with names in txt files
# Need to clean the names before using


def stripping(strings: str):
    """."""
    if " (" in strings:
        strings = strings.split(" (")[0]
    if "[b]" in strings:
        strings = strings.split("[")[0]
    if "[a]" in strings:
        strings = strings.split("[")[0]
    if "[c]" in strings:
        strings = strings.split("[")[0]
    if "[d]" in strings:
        strings = strings.split("[")[0]
    if "[e]" in strings:
        strings = strings.split("[")[0]
    if "[g]" in strings:
        strings = strings.split("[")[0]
    if "[f]" in strings:
        strings = strings.split("[")[0]
    if "Cup Winners' Cup" in strings:
        strings = ""
    if "Mitropa" in strings:
        strings = ""
    if "Readmitted" in strings:
        strings = ""
    if "[1]" in strings:
        strings = strings.split("[")[0]
    if "Segunda" in strings:
        strings = ""

    return strings.strip("\n").strip()


def correct_names(strings: str):
    """."""
    if strings == "Milan":
        strings = "AC Milan"
    elif strings == "Inter Milan":
        strings = "Internazionale"
    elif strings == "Inter":
        strings = "Internazionale"
    elif strings == "ChievoVerona":
        strings = "Chievo"
    elif strings == "Paris SG":
        strings = "Paris Saint-Germain"
    # corrected1[corrected1["Team"] == "Deportivo de La Coruña"] = "Deportivo La Coruña"
    # corrected1[corrected1["Team"] == "FC Barcelona"] = "Barcelona"
    # corrected1[corrected1["Team"] == "Valencia CF"] = "Valencia"
    # corrected1[corrected1["Team"] == "CD Tenerife"] = "CD Tenerife"
    # corrected1[corrected1["Team"] == "Hércules CF"] = "Hércules"
    # corrected1[corrected1["Team"] == "Racing de Santander"] = "Racing Santander"
    # corrected1[corrected1["Team"] == "Celta de Vigo"] = "Celta Vigo"
    # corrected1[corrected1["Team"] == "CD Tenerife"] = "Tenerife"
    # corrected1[corrected1["Team"] == "Sevilla FC"] = "Sevilla"
    # corrected1[corrected1["Team"] == "UD Salamanca"] = "Salamanca"
    # corrected1[corrected1["Team"] == "RCD Espanyol"] = "Espanyol"
    # corrected1[corrected1["Team"] == "SD Compostela"] = "Compostela"
    # corrected1[corrected1["Team"] == "Sporting de Gijón"] = "Sporting Gijón"
    # corrected1[corrected1["Team"] == "CF Extramadura"] = "Extramadura"
    # corrected1[corrected1["Team"] == "Sporting de Gijón"] = "Sporting Gijón"
    # corrected1[corrected1["Team"] == "CP Mérida"] = "Mérida"
    # corrected1[corrected1["Team"] == "CD Logroñés"] = "Logroñés"
    return strings


def clean_it(league: str):
    """."""
    path = Path.cwd() / "data" / league
    files = path.rglob("*.txt")

    for file in files:
        rewritten_file = []
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                ll = stripping(line)
                lll = correct_names(ll)
                if lll != "":
                    rewritten_file.append(lll)
        new_path = Path.cwd() / "refined_data" / league
        new_path.mkdir(parents=True, exist_ok=True)
        filepath = new_path / file.name

        with open(filepath, "w") as f:
            for item in rewritten_file:
                f.writelines(f"{item}\n")


def clean_that(league: str):
    """."""
    path = Path.cwd() / "data" / league
    files = path.rglob("*results.csv")
    for file in track(files, description="Converting..."):
        tmp_df = DataFrame(read_csv(file))
        # print(list(tmp_df["Result"]))
        tmp_df["Home"] = tmp_df["Home"].str.replace(" ", " ")  # noqa: RUF001
        tmp_df["Away"] = tmp_df["Away"].str.replace(" ", " ")  # noqa: RUF001
        tmp_df["Result"] = tmp_df["Result"].str.replace("−", "–")  # noqa: RUF001
        tmp_df[["HS", "AS"]] = tmp_df["Result"].str.split("–", expand=True)  # noqa: RUF001
        tmp_df = tmp_df.drop(["Result"], axis=1)
        tmp_df = tmp_df[["Home", "HS", "AS", "Away"]]

        corrected_file = []
        for row in tmp_df.values:
            for cell in row:
                val = stripping(cell)
                val = correct_names(val)
                corrected_file.append(val)
        new_file = DataFrame(reshape(corrected_file, (int(len(corrected_file) / 4), 4)))
        new_file.columns = ["Home", "HS", "AS", "Away"]
        # print(list(new_file["AS"]))
        new_file["AS"] = to_numeric(new_file["AS"], downcast="integer", errors="coerce")
        new_path = Path.cwd() / "refined_data" / league
        new_path.mkdir(parents=True, exist_ok=True)
        filepath = new_path / file.name
        new_file.to_csv(filepath, sep=",", index=False)


# clean_that("Serie_A")
