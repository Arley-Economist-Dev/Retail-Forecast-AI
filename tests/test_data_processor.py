"""Unit tests for the DataProcessor service and Nixtla contract validation."""

import pytest
import pandas as pd
from app.services.data_processor import DataProcessor, DataValidationError


def test_valid_csv_loading():
    """Verify that a compliant Nixtla CSV is parsed and validated successfully."""
    valid_csv = b"""unique_id,ds,y
SKU_TEST,2025-01-01,100.0
SKU_TEST,2025-01-02,110.0
SKU_TEST,2025-01-03,105.0
SKU_TEST,2025-01-04,120.0
SKU_TEST,2025-01-05,130.0
SKU_TEST,2025-01-06,115.0
SKU_TEST,2025-01-07,125.0
SKU_TEST,2025-01-08,105.0
SKU_TEST,2025-01-09,112.0
SKU_TEST,2025-01-10,122.0
SKU_TEST,2025-01-11,135.0
SKU_TEST,2025-01-12,140.0
SKU_TEST,2025-01-13,118.0
SKU_TEST,2025-01-14,128.0
"""
    df, active_series, available_series, freq = DataProcessor.load_and_validate_csv(valid_csv)

    assert active_series == "SKU_TEST"
    assert available_series == ["SKU_TEST"]
    assert len(df) == 14
    assert freq in ["D", "1D"]
    assert "unique_id" in df.columns
    assert "ds" in df.columns
    assert "y" in df.columns


def test_missing_required_columns():
    """Verify that missing Nixtla columns trigger DataValidationError."""
    invalid_csv = b"""item_id,date,sales
SKU_01,2025-01-01,100
"""
    with pytest.raises(DataValidationError) as exc_info:
        DataProcessor.load_and_validate_csv(invalid_csv)

    assert "columnas requeridas" in str(exc_info.value).lower()


def test_empty_csv():
    """Verify that an empty file triggers DataValidationError."""
    with pytest.raises(DataValidationError) as exc_info:
        DataProcessor.load_and_validate_csv(b"")

    assert "vacío" in str(exc_info.value).lower()


def test_insufficient_history_length():
    """Verify that series with fewer than 14 records are rejected."""
    short_csv = b"""unique_id,ds,y
SKU_01,2025-01-01,10
SKU_01,2025-01-02,20
SKU_01,2025-01-03,30
"""
    with pytest.raises(DataValidationError) as exc_info:
        DataProcessor.load_and_validate_csv(short_csv)

    assert "mínimo de 14 observaciones" in str(exc_info.value)


def test_gap_imputation():
    """Verify that missing dates in the sequence are filled with zero."""
    gapped_csv = b"""unique_id,ds,y
SKU_GAP,2025-01-01,100
SKU_GAP,2025-01-02,100
SKU_GAP,2025-01-03,100
SKU_GAP,2025-01-04,100
SKU_GAP,2025-01-05,100
SKU_GAP,2025-01-06,100
SKU_GAP,2025-01-07,100
SKU_GAP,2025-01-10,100
SKU_GAP,2025-01-11,100
SKU_GAP,2025-01-12,100
SKU_GAP,2025-01-13,100
SKU_GAP,2025-01-14,100
SKU_GAP,2025-01-15,100
SKU_GAP,2025-01-16,100
"""
    df, _, _, _ = DataProcessor.load_and_validate_csv(gapped_csv, fill_gaps=True)
    # 2025-01-01 to 2025-01-16 is 16 days
    assert len(df) == 16
    # Dates 2025-01-08 and 2025-01-09 should have y=0.0
    gap_row = df[df["ds"] == pd.to_datetime("2025-01-08")]
    assert not gap_row.empty
    assert gap_row["y"].values[0] == 0.0


def test_statistical_calculation():
    """Verify that statistics calculations (mean, cv, trend) are consistent."""
    df_hist = pd.DataFrame({
        "unique_id": ["SKU_1"] * 14,
        "ds": pd.date_range("2025-01-01", periods=14, freq="D"),
        "y": [100.0] * 14,
    })
    df_forecast = pd.DataFrame({
        "unique_id": ["SKU_1"] * 7,
        "ds": pd.date_range("2025-01-15", periods=7, freq="D"),
        "y_hat": [120.0] * 7,
    })

    stats = DataProcessor.calculate_statistics(
        df_historical=df_hist,
        forecast_df=df_forecast,
        unique_id="SKU_1",
        freq="D",
    )

    assert stats.historical_mean == 100.0
    assert stats.forecast_mean == 120.0
    assert stats.percentage_change == 20.0
    assert stats.trend_direction == "ALCISTA"
    assert stats.historical_cv == 0.0
