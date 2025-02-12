import datetime as dt
from typing import TypedDict
from typing_extensions import Unpack
import pytz


class IntervalKwargs(TypedDict):
    days: int
    seconds: int
    microseconds: int
    milliseconds: int
    minutes: int
    hours: int
    weeks: int


class DateUtils:
    """
    A utility class for handling date and time operations.

    Author: Konstantinos A.

    Date: 14 Nov 2024
    """

    def getNow():
        """
        Get the current date and time in ISO 8601 format (UTC).
        Returns:
            str: The current date and time formatted as "%Y-%m-%dT%H:%M:%SZ".

        Author: Konstantinos A.

        Date: 14 Nov 2024
        """

        return dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def getNowUtc():
        """
        Get the current date and time in UTC.
        Returns:
            str: The current date and time in UTC formatted as an ISO 8601 string (YYYY-MM-DDTHH:MM:SSZ).

        Author: Konstantinos A.
        Date: 30 Jan 2025
        """

        return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def convertDateToUTC(
        date: dt.datetime, includeSeconds: bool = False, initialTz: bool = False
    ) -> str:
        """
        Convert the given date to UTC.

        Args:
            date (dt.datetime): The date to convert.

        Returns:
            str: The date converted to UTC.

        Author: Konstantinos A.
        Date: 28 Jan 2025
        """
        if initialTz:
            date = date.astimezone(pytz.timezone("Europe/Athens"))
        dateFmt = "%Y-%m-%dT%H:%MZ" if not includeSeconds else "%Y-%m-%dT%H:%M:%SZ"
        return date.astimezone(dt.timezone.utc).strftime(dateFmt)

    def getDateFromUTC(date: str, format: str = "%Y-%m-%dT%H:%MZ") -> dt.datetime:
        """
        Convert the given UTC date string to a datetime object with timezone.

        Args:
            date (str): The date string to convert.
            format (str): The format of the date string. Defaults to YYYY-MM-DDTHH:MMZ.
        Returns:
            dt.datetime: The datetime object.
        """
        dateUtc = dt.datetime.strptime(date, format)
        return pytz.timezone("Europe/Athens").localize(dateUtc)

    def getUTCDateTime():
        """
        Get the current date and time in UTC.
        Returns:
            str: The current date and time in UTC formatted as an ISO 8601 string (YYYY-MM-DDTHH:MM:SSZ).

        Author: Konstantinos A.

        Date: 14 Nov 2024
        """

        return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

    def getFormattedDateRange(start_date, end_date):
        """
        Returns a formatted date range string if both start_date and end_date are valid.
        Args:
            start_date (str): The start date in the format 'YYYY-MM-DDTHH:MMZ'.
            end_date (str): The end date in the format 'YYYY-MM-DDTHH:MMZ'.
        Returns:
            str: A formatted string representing the date range in the format 'start_date/end_date'.
        Raises:
            ValueError: If either start_date or end_date is not in the valid format.

        Author: Konstantinos A.

        Date: 14 Nov 2024
        """

        if DateUtils.validateDateTime(start_date) and DateUtils.validateDateTime(end_date):
            return f"{start_date}/{end_date}"
        else:
            raise ValueError(
                "Invalid date format, date should be in the format of 'YYYY-MM-DDTHH:MMZ'"
            )

    def validateDateTime(date_time):
        """
        Validates if the given date_time string matches the format "%Y-%m-%dT%H:%MZ".
        Args:
            date_time (str): The date and time string to validate.
        Returns:
            bool: True if the date_time string matches the format, False otherwise.

        Author: Konstantinos A.

        Date: 14 Nov 2024
        """

        try:
            dt.datetime.strptime(date_time, "%Y-%m-%dT%H:%MZ")
        except ValueError:
            return False
        return True

    def getDateRangeIntervals(start_date, end_date, **kwargs: Unpack[IntervalKwargs]):
        """
        Generates intervals of date ranges between the given start and end dates.
        Args:
            start_date (str): The start date in the format 'YYYY-MM-DDTHH:MMZ'.
            end_date (str): The end date in the format 'YYYY-MM-DDTHH:MMZ'.
            **kwargs: Additional keyword arguments to specify the interval step (e.g., days=1, hours=2).
        Yields:
            tuple: A tuple containing the interval index, start date, and end date of the interval in the format 'YYYY-MM-DDTHH:MMZ'.
        Raises:
            ValueError: If the start_date or end_date is not in the correct format.

        Author: Konstantinos A.

        Date: 15 Nov 2024
        """

        if DateUtils.validateDateTime(start_date) and DateUtils.validateDateTime(end_date):
            start = dt.datetime.strptime(start_date, "%Y-%m-%dT%H:%MZ")
            end = dt.datetime.strptime(end_date, "%Y-%m-%dT%H:%MZ")
            step = dt.timedelta(**kwargs)
            i = 1
            while start < end:
                endInt = start + step
                yield (i, start.strftime("%Y-%m-%dT%H:%MZ"), endInt.strftime("%Y-%m-%dT%H:%MZ"))
                start += step
                i += 1
        else:
            raise ValueError(
                "Invalid date format, date should be in the format of 'YYYY-MM-DDTHH:MMZ'"
            )
