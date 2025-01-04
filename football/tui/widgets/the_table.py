"""Pandas DataFrame to textual DataTable."""

from pandas import DataFrame
from textual.widgets import DataTable


class FootballDataTable(DataTable):
    """Format football df."""

    def add_df(self, df: DataFrame):
        """Get the df."""
        self.df = df
        self.add_columns(*self._add_df_columns())
        self.add_rows(self._add_df_rows()[0:])
        return self

    def update_df(self, df: DataFrame):
        """Update df."""
        self.clear(columns=True)
        self.add_df(df)

    def _add_df_rows(self):
        return self._get_df_rows()

    def _add_df_columns(self):
        return self._get_df_columns()

    def _get_df_rows(self):
        return list(self.df.itertuples(index=False, name=None))

    def _get_df_columns(self) -> tuple:
        return tuple(self.df.columns.values.tolist())
