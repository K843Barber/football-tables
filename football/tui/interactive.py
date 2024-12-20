from football.helper_functions import convert_data_to_df  # noqa: D100
from football.show_table import all_time_table
from football.tui.football_app import FootballAppV2


def interactive(league, start, end):
    """."""
    if int(end) - int(start) == 1:
        df = convert_data_to_df(league, start, end)
        FootballAppV2(df, league, start, end, False).run()
    else:
        seasons = [str(i) for i in range(int(start), int(end), 1)]
        df = all_time_table(league, seasons)
        FootballAppV2(df, league, start, end, True).run()
