"""."""

import os


def test_entrypoint():
    """."""
    exit_status = os.system("football --help")  # noqa: S605, S607
    assert exit_status == 0
