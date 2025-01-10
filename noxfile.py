"""."""

import nox


@nox.session
def tests(session):
    """."""
    session.install(
        "pytest", "pandas", "rich", "textual_serve", "textual_plotext", "pytest-asyncio"
    )
    session.run("pytest")


@nox.session
def lint(session):
    """."""
    session.install("ruff")
    session.run("ruff", "check", "--fix", "--unsafe-fixes", "--config", "pyproject.toml")
