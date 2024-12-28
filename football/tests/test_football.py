import pytest  # noqa: D100

from football.tui.football_app import FootballApp


@pytest.mark.asyncio
async def test_buttons():
    """."""
    app = FootballApp()
    async with app.run_test() as pilot:
        await pilot.click("#quit")
        assert app.screen.name is None  # noqa: S101
