"""Some of the screens."""

from rich.console import Console
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import (
    Button,
    Header,
    MarkdownViewer,
    Static,
)

from football.common.readme import MARKDOWN

console = Console()


class QuitScreen(Screen):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Grid(
            Static("You wanna Quit?", id="question"),
            Button("Yes", variant="error", id="yes"),
            Button("No", variant="success", id="no"),
            id="quit_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed):
        """."""
        if event.button.id == "yes":
            self.app.exit()
        else:
            self.dismiss(True)


class ContentScreen(Screen):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield Header()
        yield Grid(
            Button("Tables and Stats", id="Tables"),
            Button("Head 2 Head", id="h2h", classes="H2HINIT"),
            Button("Individual Team", id="invidual_team"),
            Button("All Time", id="allatida"),
            Button("Back", id="back"),
            id="what_we_got",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "back":
            self.dismiss(True)


class ReadMeScreen(Screen):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def compose(self) -> ComposeResult:
        """."""
        yield MarkdownViewer(MARKDOWN, show_table_of_contents=True)
        yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """."""
        if event.button.id == "back":
            self.dismiss(True)
