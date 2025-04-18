import pandas as pd


class CommonDataFrames:

    @staticmethod
    def create_empty_timestamp_df(today: str, colName: str = "timestamp") -> pd.DataFrame:
        """
        Creates an empty DataFrame with a timestamp column containing half-hourly intervals for a given day.

        Parameters:
            today (str): The starting date in the format 'YYYY-MM-DD'.
            colName (str, optional): The name of the timestamp column. Defaults to "timestamp".

        Returns:
            pd.DataFrame: A DataFrame with a single column of half-hourly timestamps for the specified day.
        """
        halfHourly = pd.date_range(today, periods=48, freq="30min")
        df = halfHourly.to_frame(index=False).rename(columns={0: colName})
        return df
