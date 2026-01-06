# test_datagraph.py
import pytest
import pandas as pd

from datagraph import (
    load_activity_data,
    compute_basic_stats,
    DataValidationError,
)


VALID_CSV = """timestamp,steps,heart_rate,sleep_duration
2026-01-01 08:00:00,8500,72,7.5
2026-01-02 08:00:00,9200,75,8.0
"""


# ---------- Data ingestion tests ----------

def test_load_activity_data_success():
    df = load_activity_data(VALID_CSV)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["timestamp", "steps", "heart_rate", "sleep_duration"]
    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])


def test_load_activity_data_empty_raises():
    with pytest.raises(DataValidationError):
        load_activity_data("   ")


def test_load_activity_data_missing_column_raises():
    bad_csv = """timestamp,steps,heart_rate
2026-01-01 08:00:00,8500,72
"""
    with pytest.raises(DataValidationError):
        load_activity_data(bad_csv)


def test_load_activity_data_negative_steps_raises():
    bad_csv = """timestamp,steps,heart_rate,sleep_duration
2026-01-01 08:00:00,-10,72,7.5
"""
    with pytest.raises(DataValidationError):
        load_activity_data(bad_csv)


def test_load_activity_data_invalid_timestamp_raises():
    bad_csv = """timestamp,steps,heart_rate,sleep_duration
not-a-date,8500,72,7.5
"""
    with pytest.raises(DataValidationError):
        load_activity_data(bad_csv)


# ---------- Analysis function tests ----------

def test_compute_basic_stats_values():
    df = load_activity_data(VALID_CSV)
    stats = compute_basic_stats(df)

    assert pytest.approx(stats["mean_steps"]) == (8500 + 9200) / 2
    assert stats["max_steps"] == 9200
    assert stats["min_steps"] == 8500
    assert pytest.approx(stats["mean_heart_rate"]) == (72 + 75) / 2
    assert pytest.approx(stats["mean_sleep"]) == (7.5 + 8.0) / 2


def test_compute_basic_stats_empty_df_raises():
    empty_df = pd.DataFrame(
        columns=["timestamp", "steps", "heart_rate", "sleep_duration"]
    )
    with pytest.raises(ValueError):
        compute_basic_stats(empty_df)
