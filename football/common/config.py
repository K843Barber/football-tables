"""Configuration file."""

import json
from json import dump
from pathlib import Path

from inquirer import Checkbox, Text, prompt
from rich import print
from rich.emoji import Emoji
from rich.panel import Panel


def configuration():
    """."""
    path = Path.cwd() / ".config"
    path.mkdir(parents=True, exist_ok=True)
    file = path / "config.json"
    print(
        Panel(
            "",
            title="[cyan]Football League Configuration![/cyan]",
            title_align="center",
            style="bold cyan on magenta",
        ),
    )
    league = [
        Checkbox(
            "league",
            message=f"{Emoji('football')} Which leagues would you like to see? {Emoji('football')}",  # noqa: E501
            choices=[
                "Allsvenskan",
                "Bundesliga",
                "Eredivisie",
                "Football_League_First_Division",
                "La_Liga",
                "Ligue_1",
                "Premier_League",
                "Serie_A",
            ],
        ),
        Text(
            "season",
            message="Which is the latest season?",
            default="2024",
        ),
    ]

    with open(file, "w", encoding="utf-8") as f:
        dump(prompt(league), f, indent=4)


def load_config():
    """Load config file."""
    config_file = Path.cwd() / ".config/config.json"

    with open(config_file) as f:
        d = json.load(f)

    return d["league"], d["season"]
