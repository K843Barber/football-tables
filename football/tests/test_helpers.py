"""."""

import logging
import os
from pathlib import Path
from random import SystemRandom
from string import ascii_lowercase

import pytest
from pandas import DataFrame
from rich.table import Table

from football.common.all_time_helper import all_time_table, get_smallest, league_winners
from football.common.helper_functions import convert_data_to_df

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@pytest.fixture(autouse=True)
def clean_environment(league: str):
    """."""
    path = Path.cwd() / "refined_data" / league

    logger.info(msg="Check to see if filepath exists.")
    logger.debug(" If it exists, clean up is incorrect")
    assert path.exists() is False, "folder not cleaned up properly"

    logger.info(msg="See if there are any files to remove")
    logger.debug(msg="List should be empty from a proper cleanup")
    files = list(path.rglob("*.txt"))
    assert len(files) == 0, "List not empty, clean has failed in previous tests"

    logger.info(msg="Check to see if folders are there to remove")
    logger.debug(msg="If folder exists, clean up has not properly executed")
    assert os.path.exists(path) is False, "Nope, file does not exist"

    yield

    path = Path.cwd() / "refined_data" / league

    logger.info(msg="Check to see if filepath exists")
    assert path.exists(), "folder doesn't exist"

    files = list(path.rglob("*.txt"))

    logger.info(msg="Remove them if the files exist")
    for file in files:
        os.remove(file)

    logger.info(msg="Check to see if folders are there to remove")
    if os.path.exists(path):
        os.rmdir(path)

    logger.info(msg="Remove testing folder environment")
    os.rmdir(Path.cwd() / "refined_data")

    logger.info(msg="Ensure testing folder has been removed successfully")
    assert (
        os.path.exists(Path.cwd() / "refined_data") is False
    ), "Unsuccessfully removed testing folder"
    logger.info(msg="Folder removed successfully")


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """."""
    monkeypatch.chdir(request.fspath.dirname)


@pytest.mark.parametrize(
    "league",
    ["Premier_League", "Ligue_1", "Serie_A", "Bundesliga", "La_Liga", "Allsvenskan"],
)
@pytest.mark.usefixtures("clean_environment")
def test_get_smallest(league: str):
    """."""
    logger.info(msg="Creating filepaths")
    d = Path.cwd() / "refined_data" / league
    d.mkdir(parents=True, exist_ok=True)
    assert d.exists()
    cryptogen = SystemRandom()

    logger.info(msg="Initialising lists")
    randers = [cryptogen.randrange(10, 100) for _ in range(10)]
    rando = [f"{i}_{i+1}" for i in randers]

    logger.info(msg="Creating and writing to files")
    for i in rando:
        p = d / f"{i}.txt"
        p.write_text("content", encoding="utf-8")

    logger.info(msg="Asserting function gets the smallest value")
    assert min(randers) == get_smallest(league), "Function didn't output correct values"


@pytest.mark.parametrize(
    "league",
    [
        "Premier_League",
        "Ligue_1",
        "Serie_A",
        "Bundesliga",
        "La_Liga",
        "Allsvenskan",
    ],
)
def test_txt_to_df(league: str):
    """."""
    logger.info(msg="Create folder")
    path = Path.cwd() / "refined_data" / league
    path.mkdir(parents=True, exist_ok=True)
    assert path.exists()
    logger.info(msg="Define file")
    file = path / "1992_1993.txt"
    logger.info(msg="Open folder and write data")
    crypt = SystemRandom()
    with open(file, "w") as f:
        for i in range(200):
            if i % 10 == 1:
                f.writelines(
                    f"{''.join(crypt.choice(ascii_lowercase) for _ in range(10))}\n"
                )
            else:
                f.writelines(f"{SystemRandom().randrange(-10, 50)}\n")
    logger.info(msg="Check shape of dataframe")
    df = convert_data_to_df(league, "1992", "1993")

    assert df.shape == (20, 10), "DataFrame is not of shape 20 10"


@pytest.mark.parametrize("league", ["Premier_League"])
def test_winners(league: str):
    """."""
    logger.info("Create txt files with data")
    logger.info(msg="Create folder")
    path = Path.cwd() / "refined_data" / league
    path.mkdir(parents=True, exist_ok=True)
    assert path.exists()

    logger.info(msg="Define file")
    files = [f"{i}_{i+1}.txt" for i in range(1992, 2000)]

    logger.info(msg="Open folder and write data")

    leaders: dict = {}
    for file in files:
        filepath = path / file

        crypt = SystemRandom()
        with open(filepath, "w") as f:
            for i in range(200):
                if i % 10 == 0:
                    team = "".join(crypt.choice(ascii_lowercase) for _ in range(10))
                    f.writelines(f"{team}\n")
                    if i == 0:
                        if team in leaders:
                            leaders[team] += 1
                        else:
                            leaders[team] = 1
                else:
                    f.writelines(f"{SystemRandom().randrange(-10, 50)}\n")

    # teams = sorted(leaders)

    assert isinstance(league_winners(league), Table)


@pytest.mark.parametrize("league", ["Premier_League"])
def test_all_time_helperv2(league: str):
    """."""
    logger.info("Create path for files")
    path = Path.cwd() / "refined_data" / league
    path.mkdir(parents=True, exist_ok=True)
    assert path.exists(), "Path not created"

    logger.info("Create files")
    files = [f"{i}_{i+1}.txt" for i in range(1992, 1994)]
    for file in files:
        filepath = path / file
        crypt = SystemRandom()

        logger.info("Write to the files")
        with open(filepath, "w") as f:
            for i in range(200):
                if i % 10 == 0:
                    team = "".join(crypt.choice(ascii_lowercase) for _ in range(10))
                    f.writelines(f"{team}\n")
                else:
                    f.writelines(f"{SystemRandom().randrange(-10, 50)}\n")

    assert isinstance(
        all_time_table(league, ["1992", "1993"]), DataFrame
    ), "Instance is not a dataframe"
