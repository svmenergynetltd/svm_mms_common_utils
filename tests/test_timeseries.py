import datetime as dt

import pandas as pd
import pytest

from svm_mms_common_utils.constants import MMS_CONSTANTS
from svm_mms_common_utils.enums import PowerUnits
from svm_mms_common_utils.utils.timeseries import TimeSeriesUtils


def _series():
    return [
        {"timestamp": "2024-01-15T13:00:00", "quantity": 1.23456, "price": None},
        {"timestamp": "2024-01-15T12:00:00", "quantity": 2.5, "price": 10.1294},
    ]


def test_round_to_mms_decimals_rounds_requested_keys_and_keeps_none():
    original = _series()

    rounded = TimeSeriesUtils.round_to_mms_decimals(original, ["quantity", "price"])

    assert rounded[0]["quantity"] == round(1.23456, MMS_CONSTANTS.DECIMALS)
    assert rounded[0]["price"] is None
    assert rounded[1]["price"] == round(10.1294, MMS_CONSTANTS.DECIMALS)
    assert original[0]["quantity"] == 1.23456
    assert rounded[0] is not original[0]


def test_round_to_mms_decimals_requires_every_key():
    with pytest.raises(ValueError, match="not found in series"):
        TimeSeriesUtils.round_to_mms_decimals(_series(), ["quantity", "missing"])


def test_round_to_mms_decimals_requires_a_point():
    with pytest.raises(IndexError):
        TimeSeriesUtils.round_to_mms_decimals([], ["quantity"])


@pytest.mark.parametrize(
    ("source", "target", "factor"),
    [
        (PowerUnits.MW, PowerUnits.KW, 1000),
        (PowerUnits.KW, PowerUnits.MW, 1 / 1000),
        (PowerUnits.MWH, PowerUnits.KWH, 1000),
        (PowerUnits.KWH, PowerUnits.MWH, 1 / 1000),
        (PowerUnits.MWH, PowerUnits.MW, 2),
        (PowerUnits.MW, PowerUnits.MWH, 1 / 2),
        (PowerUnits.KW, PowerUnits.KW, 1),
        (PowerUnits.MWH, PowerUnits.MWH, 1),
    ],
)
def test_conversion_factor(source, target, factor):
    assert TimeSeriesUtils.get_conversion_factor(source, target) == factor


@pytest.mark.parametrize(
    ("source", "target"),
    [
        (PowerUnits.KW, PowerUnits.MWH),
        (PowerUnits.KWH, PowerUnits.MW),
        (PowerUnits.MW, PowerUnits.KWH),
        (PowerUnits.MWH, PowerUnits.KW),
        (PowerUnits.KW, PowerUnits.KWH),
    ],
)
def test_conversion_factor_rejects_unsupported_pairs(source, target):
    with pytest.raises(ValueError, match=f"Conversion from {source} to {target} not supported"):
        TimeSeriesUtils.get_conversion_factor(source, target)


def test_convert_to_unit_scales_values_and_preserves_none():
    original = [
        {"timestamp": "2024-01-15T12:00:00", "quantity": 1.5},
        {"timestamp": "2024-01-15T12:30:00", "quantity": None},
    ]

    converted = TimeSeriesUtils.convert_to_unit(
        original,
        "quantity",
        PowerUnits.MW,
        PowerUnits.MWH,
    )

    assert converted[0]["quantity"] == 0.75
    assert converted[1]["quantity"] is None
    assert original[0]["quantity"] == 1.5


def test_convert_to_unit_defaults_to_megawatt_hours():
    converted = TimeSeriesUtils.convert_to_unit(
        [{"quantity": 4}],
        "quantity",
        PowerUnits.MW,
    )

    assert converted[0]["quantity"] == 2


def test_convert_to_unit_requires_the_value_key():
    with pytest.raises(ValueError, match="Value key quantity not found"):
        TimeSeriesUtils.convert_to_unit([{"price": 1}], "quantity", PowerUnits.MW)


def test_convert_to_unit_requires_a_point():
    with pytest.raises(IndexError):
        TimeSeriesUtils.convert_to_unit([], "quantity", PowerUnits.MW)


def test_get_start_end_dates_uses_athens_for_naive_timestamps_and_adds_thirty_minutes():
    series = [
        {"timestamp": "2024-01-15T12:00:00", "quantity": 1},
        {"timestamp": "2024-01-15T13:00:00", "quantity": 2},
    ]

    start, end = TimeSeriesUtils.get_start_end_dates(series)

    assert start == "2024-01-15T10:00Z"
    assert end == "2024-01-15T11:30Z"
    assert series[0]["timestamp"] == "2024-01-15T12:00:00"


def test_get_start_end_dates_keeps_aware_timestamps_in_utc():
    series = [
        {"timestamp": dt.datetime(2024, 7, 15, 9, 0, tzinfo=dt.timezone.utc)},
        {"timestamp": dt.datetime(2024, 7, 15, 9, 30, tzinfo=dt.timezone.utc)},
    ]

    assert TimeSeriesUtils.get_start_end_dates(series) == (
        "2024-07-15T09:00Z",
        "2024-07-15T10:00Z",
    )


def test_get_start_end_dates_reads_a_custom_key():
    series = [
        {"ts": "2024-07-15T12:00:00"},
        {"ts": "2024-07-15T12:30:00"},
    ]

    assert TimeSeriesUtils.get_start_end_dates(series, key="ts") == (
        "2024-07-15T09:00Z",
        "2024-07-15T10:00Z",
    )


def test_sort_by_timestamp_returns_a_new_chronological_list():
    original = _series()

    ordered = TimeSeriesUtils.sort_by_timestamp(original)

    assert [point["timestamp"] for point in ordered] == [
        "2024-01-15T12:00:00",
        "2024-01-15T13:00:00",
    ]
    assert [point["timestamp"] for point in original] == [
        "2024-01-15T13:00:00",
        "2024-01-15T12:00:00",
    ]


def test_sort_by_timestamp_accepts_a_custom_key():
    ordered = TimeSeriesUtils.sort_by_timestamp(
        [{"slot": 2}, {"slot": 1}],
        key="slot",
    )

    assert [point["slot"] for point in ordered] == [1, 2]


def test_compare_time_series_lists_changed_fields():
    left = [
        {"timestamp": "2024-01-15T12:00Z", "quantity": 1, "price": 10},
        {"timestamp": "2024-01-15T12:30Z", "quantity": 2, "price": 11},
    ]
    right = [
        {"timestamp": "2024-01-15T12:00Z", "quantity": 1.5, "price": 10},
        {"timestamp": "2024-01-15T13:00Z", "quantity": 2, "price": 12},
    ]

    changes = set(TimeSeriesUtils.compare_time_series(left, right).split(", "))

    assert changes == {
        "Changed quantity at 2024-01-15T12:00Z from 1 to 1.5",
        "Changed timestamp at 2024-01-15T12:30Z from 2024-01-15T12:30Z to 2024-01-15T13:00Z",
        "Changed price at 2024-01-15T12:30Z from 11 to 12",
    }


def test_compare_time_series_returns_an_empty_string_when_equal():
    series = [{"timestamp": "2024-01-15T12:00Z", "quantity": 1}]

    assert TimeSeriesUtils.compare_time_series(series, [series[0].copy()]) == ""


def test_compare_time_series_requires_matching_keys():
    with pytest.raises(ValueError, match="Time series keys do not match"):
        TimeSeriesUtils.compare_time_series(
            [{"timestamp": "t", "quantity": 1}],
            [{"timestamp": "t", "price": 1}],
        )


def test_compare_time_series_requires_aligned_lengths():
    with pytest.raises(IndexError):
        TimeSeriesUtils.compare_time_series(
            [{"timestamp": "t", "quantity": 1}, {"timestamp": "t2", "quantity": 2}],
            [{"timestamp": "t", "quantity": 1}],
        )


def test_get_series_total_sums_numeric_values_and_treats_none_as_zero():
    series = [{"quantity": 1}, {"quantity": "2.5"}, {"quantity": None}]

    assert TimeSeriesUtils.get_series_total(series, "quantity") == 3.5


def test_get_series_total_of_an_empty_series_is_zero():
    assert TimeSeriesUtils.get_series_total([], "quantity") == 0


def test_get_series_total_requires_the_column():
    with pytest.raises(ValueError, match="Column key quantity not found"):
        TimeSeriesUtils.get_series_total([{"price": 1}], "quantity")


def test_apply_curtailed_quantities_updates_one_based_indexes():
    series = [
        {"timestamp": "t1", "quantity": 1},
        {"timestamp": "t2", "quantity": 2},
        {"timestamp": "t3", "quantity": 3},
    ]
    curtailed = [
        {"timeseries_id": "ts-1", "timestamp_index": 1, "quantity": 10},
        {"timeseries_id": "ts-1", "timestamp_index": "3", "quantity": 30},
        {"timeseries_id": "ts-1", "timestamp_index": 0, "quantity": 99},
        {"timeseries_id": "ts-1", "timestamp_index": 4, "quantity": 99},
    ]

    updated = TimeSeriesUtils.apply_curtailed_quantities(series, curtailed)

    assert updated is series
    assert [point["quantity"] for point in series] == [10, 2, 30]


def test_apply_curtailed_quantities_accepts_a_custom_value_key():
    series = [{"power": 5}, {"power": 6}]

    TimeSeriesUtils.apply_curtailed_quantities(
        series,
        [{"timeseries_id": "ts", "timestamp_index": 2, "quantity": 8}],
        value_key="power",
    )

    assert series[1]["power"] == 8


def test_isoformat_series_converts_datetime_and_timestamp_values():
    moment = dt.datetime(2024, 1, 15, 10, 0, tzinfo=dt.timezone.utc)
    timestamp = pd.Timestamp("2024-01-15 12:00", tz="Europe/Athens")
    series = [
        {"timestamp": moment, "note": "keep"},
        {"timestamp": timestamp},
        {"timestamp": "already-text"},
        {"timestamp": dt.date(2024, 1, 15)},
        {"other": moment},
    ]

    converted = TimeSeriesUtils.isoformat_series(series)

    assert converted is series
    assert series[0]["timestamp"] == "2024-01-15T10:00:00+00:00"
    assert series[1]["timestamp"] == "2024-01-15T12:00:00+02:00"
    assert series[2]["timestamp"] == "already-text"
    assert series[3]["timestamp"] == dt.date(2024, 1, 15)
    assert series[4]["other"] == moment


def test_isoformat_series_uses_a_custom_key():
    series = [{"slot": dt.datetime(2024, 1, 15, 8, 30)}]

    TimeSeriesUtils.isoformat_series(series, key="slot")

    assert series[0]["slot"] == "2024-01-15T08:30:00"
