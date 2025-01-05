"""."""

import logging
import os
from pathlib import Path
from random import SystemRandom

import pytest

from football.common.all_time_helper import get_smallest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@pytest.fixture(autouse=True)
def clean_environment(league: str):
    """."""
    path = Path.cwd() / "refined_data" / league
    files = list(path.rglob("*.txt"))
    for file in files:
        os.remove(file)


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """."""
    monkeypatch.chdir(request.fspath.dirname)


@pytest.mark.parametrize(
    "league",
    ["Premier_League", "Ligue_1", "Serie_A", "Bundesliga", "La_Liga", "Allsvenskan"],
)
def test_get_smallest(league: str):
    """."""
    logger.log(level=1, msg="Ensure files are cleared")
    cl = Path.cwd() / "refined_data" / league
    files = cl.rglob("*.txt")
    [os.remove(f) for f in files]  # type: ignore
    cl.rmdir()
    assert not os.path.exists(Path.cwd() / "refined_data" / league)

    logger.log(level=1, msg="Creating filepaths")
    d = Path.cwd() / "refined_data" / league
    d.mkdir(parents=True, exist_ok=True)
    cryptogen = SystemRandom()

    logger.log(level=1, msg="Initialising lists")
    randers = [cryptogen.randrange(10, 100) for _ in range(10)]
    rando = [f"{i}_{i+1}" for i in randers]

    logger.log(level=1, msg="Creating and writing to files")
    for i in rando:
        p = d / f"{i}.txt"
        p.write_text("content", encoding="utf-8")

    logger.log(level=1, msg="Asserting function gets the smallest value")
    assert min(randers) == get_smallest(league), "Function didn't output correct values"
