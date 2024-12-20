from pathlib import Path
from textual.app import App, ComposeResult  # noqa: D100
from textual.widgets import Button


def read_files():
    """."""
    path = Path.cwd() / "data"

    folders = path.glob("*/")

    leagues = [str(i).split("/")[-1] for i in folders]
    return leagues


class MainApp(App):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        for league in read_files():
            yield Button(str(league))
