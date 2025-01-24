"""Remove unwanted files."""

from collections import defaultdict
from itertools import chain
from pathlib import Path

from inquirer import Checkbox, prompt
from rich import print
from rich.emoji import Emoji
from rich.tree import Tree


def walk(root, depth: int = 9):
    """."""
    tree = Tree("root 📁")
    stack = [(Path(root), tree)]

    while stack:
        path, node = stack.pop()

        if len(path.parts) >= depth:
            continue

        for child in path.iterdir():
            if child.is_dir():
                stack.append((child, node.add(f"{Emoji('folder')} {child.name}")))
            else:
                node.add(f" [magenta] {child.name}[/magenta]")

    return tree


def prune_leagues():
    """."""
    leagues = defaultdict(list)

    for j in Path(".").glob("**/*"):
        leagues[".".join((*j.parts[1:-1], j.stem))].append(j)

    answers = prompt(
        [
            Checkbox(
                "leagues",
                message="Select seasons to remove",
                choices=sorted(leagues.keys()),
                ignore=not len(leagues),
            )
        ]
    )

    if not answers:
        raise SystemExit()

    if not answers.get("leagues"):
        print("No leagues to prune, exiting")
        raise SystemExit()

    for league in chain(*map(leagues.__getitem__, answers["leagues"])):
        if league.is_file():
            print(f"Removing {league}")
            league.unlink()
        else:
            print("Removing tree", walk(league))
            for f in league.glob("**/*"):
                f.unlink()
            league.rmdir()
