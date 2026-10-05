import datetime as dt
import re

import pandas as pd
import pytest
import pytz

from svm_mms_common_utils.utils.dates import DateUtils

ATHENS = pytz.timezone("Europe/Athens")
UTC_STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z$")
UTC_STAMP_SECONDS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _utc(value: str, fmt: str = "%Y-%m-%dT%H:%M:%SZ") -> dt.datetime:
    return dt.datetime.strptime(value, fmt).replace(tzinfo=dt.timezone.utc)


def test_get_now_uses_local_clock_with_seconds():
    before = dt.datetime.now().replace(microsecond=0)
    value = DateUtils.getNow()
    after = dt.datetime.now().replace(microsecond=0) + dt.timedelta(seconds=1)

    assert UTC_STAMP_SECONDS.fullmatch(value)
    parsed = dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    assert before <= parsed <= after


def test_get_now_utc_is_current_utc_with_seconds():
    before = dt.datetime.now(dt.timezone.utc)
    value = DateUtils.getNowUtc()
    after = dt.datetime.now(dt.timezone.utc)

    assert UTC_STAMP_SECONDS.fullmatch(value)
    parsed = _utc(value)
    assert before - dt.timedelta(seconds=1) <= parsed <= after + dt.timedelta(seconds=1)


def test_get_utc_date_time_omits_seconds():
    before = dt.datetime.now(dt.timezone.utc).replace(second=0, microsecond=0)
    value = DateUtils.getUTCDateTime()
    after = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=1)

    assert UTC_STAMP.fullmatch(value)
    parsed = _utc(value, "%Y-%m-%dT%H:%MZ")
    assert before <= parsed <= after


@pytest.mark.parametrize(
    ("local", "expected"),
    [
        (dt.datetime(2024, 1, 15, 12, 0, 45), "2024-01-15T10:00Z"),
        (dt.datetime(2024, 7, 15, 12, 0, 45), "2024-07-15T09:00Z"),
    ],
)
def test_convert_date_to_utc_from_athens(local, expected):
    aware = ATHENS.localize(local)

    assert DateUtils.convertDateToUTC(aware) == expected
    assert DateUtils.convertDateToUTC(aware, initialTz=True) == expected


def test_convert_date_to_utc_can_include_seconds():
    aware = ATHENS.localize(dt.datetime(2024, 1, 15, 12, 0, 45))

    assert DateUtils.convertDateToUTC(aware, includeSeconds=True) == "2024-01-15T10:00:45Z"


def test_convert_date_to_utc_localizes_naive_values_to_athens():
    naive = dt.datetime(2024, 7, 15, 12, 30, 15)

    assert DateUtils.convertDateToUTC(naive, initialTz=True) == "2024-07-15T09:30Z"
    assert (
        DateUtils.convertDateToUTC(naive, includeSeconds=True, initialTz=True)
        == "2024-07-15T09:30:15Z"
    )


def test_convert_date_to_utc_keeps_aware_utc_values():
    utc = dt.datetime(2024, 1, 15, 10, 5, tzinfo=dt.timezone.utc)

    assert DateUtils.convertDateToUTC(utc) == "2024-01-15T10:05Z"
    assert DateUtils.convertDateToUTC(utc, includeSeconds=True) == "2024-01-15T10:05:00Z"


@pytest.mark.parametrize(
    ("value", "fmt", "expected_hour", "expected_offset"),
    [
        ("2024-01-15T10:00Z", "%Y-%m-%dT%H:%MZ", 12, dt.timedelta(hours=2)),
        ("2024-07-15T09:00Z", "%Y-%m-%dT%H:%MZ", 12, dt.timedelta(hours=3)),
        ("2024-01-15T10:00:30Z", "%Y-%m-%dT%H:%M:%SZ", 12, dt.timedelta(hours=2)),
    ],
)
def test_get_date_from_utc_converts_to_athens(value, fmt, expected_hour, expected_offset):
    result = DateUtils.getDateFromUTC(value, format=fmt)

    assert result.tzinfo.zone == "Europe/Athens"
    assert result.hour == expected_hour
    assert result.utcoffset() == expected_offset
    if "%S" in fmt:
        assert result.second == 30


@pytest.mark.parametrize(
    ("value", "valid"),
    [
        ("2024-01-15T00:00Z", True),
        ("2024-12-31T23:59Z", True),
        ("2024-01-15T00:00:00Z", False),
        ("2024-01-15T00:00", False),
        ("2024-13-01T00:00Z", False),
        ("15-01-2024T00:00Z", False),
        ("", False),
    ],
)
def test_validate_date_time(value, valid):
    assert DateUtils.validateDateTime(value) is valid


def test_get_formatted_date_range():
    assert (
        DateUtils.getFormattedDateRange("2024-01-15T00:00Z", "2024-01-16T00:00Z")
        == "2024-01-15T00:00Z/2024-01-16T00:00Z"
    )


@pytest.mark.parametrize(
    ("start", "end"),
    [
        ("2024-01-15", "2024-01-16T00:00Z"),
        ("2024-01-15T00:00Z", "2024-01-16"),
        ("bad", "also-bad"),
    ],
)
def test_get_formatted_date_range_rejects_invalid_values(start, end):
    with pytest.raises(ValueError, match="YYYY-MM-DDTHH:MMZ"):
        DateUtils.getFormattedDateRange(start, end)


def test_get_date_range_intervals_steps_until_the_end():
    intervals = list(
        DateUtils.getDateRangeIntervals("2024-01-15T00:00Z", "2024-01-15T02:00Z", hours=1)
    )

    assert intervals == [
        (1, "2024-01-15T00:00Z", "2024-01-15T01:00Z"),
        (2, "2024-01-15T01:00Z", "2024-01-15T02:00Z"),
    ]


def test_get_date_range_intervals_can_extend_past_the_end():
    intervals = list(
        DateUtils.getDateRangeIntervals("2024-01-15T00:00Z", "2024-01-15T01:30Z", hours=1)
    )

    assert intervals == [
        (1, "2024-01-15T00:00Z", "2024-01-15T01:00Z"),
        (2, "2024-01-15T01:00Z", "2024-01-15T02:00Z"),
    ]


def test_get_date_range_intervals_accepts_combined_timedelta_fields():
    intervals = list(
        DateUtils.getDateRangeIntervals(
            "2024-01-01T00:00Z",
            "2024-01-03T00:00Z",
            days=1,
            hours=12,
        )
    )

    assert intervals == [
        (1, "2024-01-01T00:00Z", "2024-01-02T12:00Z"),
        (2, "2024-01-02T12:00Z", "2024-01-04T00:00Z"),
    ]


@pytest.mark.parametrize(
    ("start", "end", "kwargs", "expected"),
    [
        (
            "2024-01-01T00:00Z",
            "2024-01-01T01:00Z",
            {"minutes": 30},
            [
                (1, "2024-01-01T00:00Z", "2024-01-01T00:30Z"),
                (2, "2024-01-01T00:30Z", "2024-01-01T01:00Z"),
            ],
        ),
        (
            "2024-01-01T00:00Z",
            "2024-01-15T00:00Z",
            {"weeks": 1},
            [
                (1, "2024-01-01T00:00Z", "2024-01-08T00:00Z"),
                (2, "2024-01-08T00:00Z", "2024-01-15T00:00Z"),
            ],
        ),
        ("2024-01-15T02:00Z", "2024-01-15T00:00Z", {"hours": 1}, []),
        ("2024-01-15T00:00Z", "2024-01-15T00:00Z", {"hours": 1}, []),
    ],
)
def test_get_date_range_interval_boundaries(start, end, kwargs, expected):
    assert list(DateUtils.getDateRangeIntervals(start, end, **kwargs)) == expected


def test_get_date_range_intervals_rejects_invalid_dates_when_iterated():
    intervals = DateUtils.getDateRangeIntervals("2024-01-15", "2024-01-16T00:00Z", hours=1)

    with pytest.raises(ValueError, match="YYYY-MM-DDTHH:MMZ"):
        next(intervals)


def test_convert_to_correct_tz_from_utc():
    utc = dt.datetime(2024, 1, 15, 10, 0, tzinfo=dt.timezone.utc)
    summer = dt.datetime(2024, 7, 15, 9, 0, tzinfo=dt.timezone.utc)

    winter_local = DateUtils.convert_to_correct_tz(utc)
    summer_local = DateUtils.convert_to_correct_tz(summer)
    unchanged = DateUtils.convert_to_correct_tz(utc, local_tz="UTC")

    assert winter_local.tzinfo.zone == "Europe/Athens"
    assert winter_local.hour == 12
    assert winter_local.utcoffset() == dt.timedelta(hours=2)
    assert summer_local.hour == 12
    assert summer_local.utcoffset() == dt.timedelta(hours=3)
    assert unchanged.hour == 10
    assert unchanged.utcoffset() == dt.timedelta(0)


def test_convert_to_correct_tz_accepts_pandas_timestamp():
    timestamp = pd.Timestamp("2024-01-15 10:00", tz="UTC")

    result = DateUtils.convert_to_correct_tz(timestamp)

    assert isinstance(result, dt.datetime)
    assert not isinstance(result, pd.Timestamp)
    assert result.hour == 12
    assert result.tzinfo.zone == "Europe/Athens"


def test_convert_to_correct_tz_assigns_athens_to_naive_values():
    result = DateUtils.convert_to_correct_tz(dt.datetime(2024, 1, 15, 12, 0))

    assert isinstance(result, dt.datetime)
    assert result.tzinfo.zone == "Europe/Athens"
