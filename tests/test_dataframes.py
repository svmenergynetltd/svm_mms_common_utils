import pandas as pd
import pytest

from svm_mms_common_utils.utils.dataframes import CommonDataFrames


def _half_hour_frame(day: str, column: str = "timestamp") -> pd.DataFrame:
    return CommonDataFrames.create_empty_timestamp_df(day, colName=column)


def test_empty_timestamp_frame_covers_a_normal_day():
    frame = _half_hour_frame("2024-01-15")

    assert list(frame.columns) == ["timestamp"]
    assert len(frame) == 48
    assert frame["timestamp"].iloc[0] == pd.Timestamp("2024-01-15 00:00", tz="Europe/Athens")
    assert frame["timestamp"].iloc[1] == pd.Timestamp("2024-01-15 00:30", tz="Europe/Athens")
    assert frame["timestamp"].iloc[-1] == pd.Timestamp("2024-01-15 23:30", tz="Europe/Athens")
    assert str(frame["timestamp"].dt.tz) == "Europe/Athens"
    deltas = frame["timestamp"].diff().dropna()
    assert (deltas == pd.Timedelta(minutes=30)).all()


def test_empty_timestamp_frame_uses_the_requested_column_name():
    frame = _half_hour_frame("2024-01-15", column="interval")

    assert list(frame.columns) == ["interval"]
    assert frame.index.equals(pd.RangeIndex(48))


def test_empty_timestamp_frame_skips_missing_spring_forward_hour():
    frame = _half_hour_frame("2024-03-31")
    labels = frame["timestamp"].dt.strftime("%H:%M")

    assert len(frame) == 46
    assert "02:30" in labels.tolist()
    assert "03:00" not in labels.tolist()
    assert "03:30" not in labels.tolist()
    assert "04:00" in labels.tolist()
    assert frame["timestamp"].iloc[0].utcoffset() == pd.Timedelta(hours=2)
    assert frame["timestamp"].iloc[-1].utcoffset() == pd.Timedelta(hours=3)


def test_empty_timestamp_frame_repeats_fall_back_hour():
    frame = _half_hour_frame("2024-10-27")
    labels = frame["timestamp"].dt.strftime("%H:%M")

    assert len(frame) == 50
    assert labels.tolist().count("03:00") == 2
    assert labels.tolist().count("03:30") == 2
    assert frame["timestamp"].iloc[0].utcoffset() == pd.Timedelta(hours=3)
    assert frame["timestamp"].iloc[-1].utcoffset() == pd.Timedelta(hours=2)


@pytest.mark.parametrize("day", ["2024-01-15", "2024-03-31", "2024-10-27"])
def test_empty_timestamp_frame_stays_on_thirty_minute_steps(day):
    frame = _half_hour_frame(day)
    deltas = frame["timestamp"].diff().dropna()

    assert (deltas == pd.Timedelta(minutes=30)).all()
