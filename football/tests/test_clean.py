"""."""

import logging
from random import SystemRandom, choice
from string import ascii_letters

import pytest

from football.common.clean_me import (
    correct_names,
    fix_gd,
    results_stripping,
    table_stripping,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def test_table_stripping():
    """."""
    char: str = f"{''.join(choice(ascii_letters) for _ in range(10))}[a]"  # noqa: S311

    tst: str = char[:-3]

    assert tst == table_stripping(char)


@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        ("Paris Saint-Germain (C)", "Paris Saint-Germain"),
        ("Lazi(o (CP)", "Lazi(o"),
        ("Eu)r(opa ", "Eu)r(opa"),
    ],
)
def test_strip_parentheses(strings: str, expected: str):
    """."""
    assert table_stripping(strings) == expected


@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        ("Qualified (Q)", ""),
        ("Invited (dd)", ""),
        ("Latin Cup ()", ""),
    ],
)
def test_strip_results(strings: str, expected: str):
    """."""
    assert results_stripping(strings) == expected


@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        ("Inter Milan", "Internazionale"),
        ("Celta de Vigo", "Celta Vigo"),
        ("Alavés", "Deportivo Alavés"),
    ],
)
def test_correct_team_name(strings: str, expected: str):
    """."""
    assert correct_names(strings) == expected


def test_correct_sums():
    """."""
    logger.info("Generate a list to compare results")
    crypt = SystemRandom()
    table = [crypt.randint(-10, 50) for _ in range(200)]

    logger.info("Save to list")
    gf = [table[i - 2] for i in range(8, len(table), 10)]
    ga = [table[i - 1] for i in range(8, len(table), 10)]

    summa = 0
    logger.info("Sum the goal differences")
    for i in range(20):
        summa += gf[i] - ga[i]

    table1 = fix_gd(table)

    assert sum(table1[8::10]) == summa, "Did not give the correct sum"
