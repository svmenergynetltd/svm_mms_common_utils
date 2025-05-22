from svm_mms_common_utils.enums import PowerUnits
from svm_mms_common_utils.constants import MMS_CONSTANTS
from svm_mms_common_utils.utils import DateUtils
from typing import List
import pandas as pd
import datetime as dt


class TimeSeriesUtils:

    @staticmethod
    def round_to_mms_decimals(
        series: List[dict[str, any]], keys: List[str]
    ) -> List[dict[str, any]]:
        """
        Rounds the values of the time series to the MMS decimal places.
        """

        for key in keys:
            if key not in series[0]:
                raise ValueError(f"Keys {keys} not found in series.")
            series = [
                {
                    **point,
                    key: (
                        round(point[key], MMS_CONSTANTS.DECIMALS)
                        if point[key] is not None
                        else None
                    ),
                }
                for point in series
            ]

        return series

    @staticmethod
    def convert_to_unit(
        series: List[dict[str, any]],
        valueKey: str,
        initUnit: PowerUnits,
        targetUnit: PowerUnits = PowerUnits.MWH,
    ) -> List[dict[str, any]]:
        """
        Converts the values of the time series to the target unit.
        """
        if valueKey not in series[0]:
            raise ValueError(f"Value key {valueKey} not found in series.")

        conversionFactor = TimeSeriesUtils.get_conversion_factor(initUnit, targetUnit)

        return [
            {
                **point,
                valueKey: (
                    point[valueKey] * conversionFactor if point[valueKey] is not None else None
                ),
            }
            for point in series
        ]

    @staticmethod
    def get_start_end_dates(series: List[dict[str, any]], key="timestamp") -> tuple[str, str]:
        """
        Returns the start and end dates of the time series, as UTC strings.
        """
        startDt = pd.to_datetime(series[0][key])
        endDt = pd.to_datetime(series[-1][key]) + dt.timedelta(minutes=30)
        startDate = DateUtils.convertDateToUTC(date=startDt, initialTz=True)
        endDate = DateUtils.convertDateToUTC(date=endDt, initialTz=True)

        return startDate, endDate

    @staticmethod
    def sort_by_timestamp(series: List[dict[str, any]], key="timestamp") -> List[dict[str, any]]:
        """
        Sorts the time series by the timestamp key.
        """
        return sorted(series, key=lambda x: x[key])

    @staticmethod
    def get_conversion_factor(initUnit: PowerUnits, targetUnit: PowerUnits) -> float:
        """
        Returns the conversion factor from the initial unit to the target unit.
        """

        if initUnit == targetUnit:
            return 1

        if initUnit == PowerUnits.MW and targetUnit == PowerUnits.KW:
            return 1000

        if initUnit == PowerUnits.KW and targetUnit == PowerUnits.MW:
            return 1 / 1000

        if initUnit == PowerUnits.MWH and targetUnit == PowerUnits.KWH:
            return 1000

        if initUnit == PowerUnits.KWH and targetUnit == PowerUnits.MWH:
            return 1 / 1000

        if initUnit == PowerUnits.MWH and targetUnit == PowerUnits.MW:
            return 2

        if initUnit == PowerUnits.MW and targetUnit == PowerUnits.MWH:
            return 1 / 2

        raise ValueError(f"Conversion from {initUnit} to {targetUnit} not supported.")

    @staticmethod
    def compare_time_series(
        timeseries1: list[dict[str, any]], timeseries2: list[dict[str, any]]
    ) -> str:
        """
        Compare two time series and return the differences as a change log string.

        :author: Konstantinos A.
        :date: 23 Dec 2024
        """

        keys1 = set(timeseries1[0].keys())
        keys2 = set(timeseries2[0].keys())

        if keys1 != keys2:
            raise ValueError("Time series keys do not match")

        differences = []

        for i in range(len(timeseries1)):
            for key in keys1:
                if timeseries1[i][key] != timeseries2[i][key]:
                    differences.append(
                        f"Changed {key} at {timeseries1[i]['timestamp']} from {timeseries1[i][key]} to {timeseries2[i][key]}"
                    )

        return ", ".join(differences)

    @staticmethod
    def get_series_total(series: list[dict[str, any]], columnKey: str) -> float:
        """Get the total of a series.

        :param series: A list of dictionaries containing the series.
        :type series: list[dict[str, Any]]
        :param columnKey: The key of the column to sum.
        :type columnKey: str

        :return: The total of the series.

        :author: Konstantinos A.
        :date: 23 Dec 2024
        """
        if not series:
            return 0

        if columnKey not in series[0].keys():
            raise ValueError(f"Column key {columnKey} not found in series")

        return sum([float(item[columnKey] or 0) for item in series])
