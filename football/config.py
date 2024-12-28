from json import dump  # noqa: D100

from inquirer import Checkbox, prompt

q = [
    Checkbox(
        "league",
        message="Which leagues would you like to see?",
        choices=["Bundesliga", "La_Liga", "Ligue_1", "Premier_League", "Serie_A"],
    )
]

with open(".config/configuration.json", "w", encoding="utf-8") as f:
    dump(prompt(q), f, indent=4)
