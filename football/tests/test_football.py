"""tests."""

# import unittest
import logging

import pytest

from football.tui.football_app import FootballApp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@pytest.mark.asyncio
async def test_buttons():
    """."""
    logger.log(level=1, msg="Initialise app")
    app = FootballApp()
    async with app.run_test() as pilot:
        logger.log(level=1, msg="Click the quit button")
        await pilot.click("#quit")
        logger.log(level=1, msg="Check that screen title is None")
        assert app.screen.name is None
        logger.log(level=1, msg="Return to home screen")
        await pilot.click("#no")
        logger.log(level=1, msg="Go to README screen")
        await pilot.click("#readme")
        assert app.screen.name is None
        await pilot.click("#back")
        assert app.screen.name is None


@pytest.mark.asyncio
@pytest.mark.skip
async def test_other_buttons():
    """."""
    logger.log(level=1, msg="Initialise app")
    app = FootballApp()
    async with app.run_test() as pilot:
        await pilot.click("#Tables")
        assert app.screen.name is None
