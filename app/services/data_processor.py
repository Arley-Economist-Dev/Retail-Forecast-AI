"""Data processing, validation and enrichment service for Nixtla-compliant time series."""

import io
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from app.schemas.forecast import DataPoint, SeriesDescriptiveStats


class DataValidationError(Exception):
    """Raised when CSV input does not adhere to the expected schema or data quality rules."""

    pass


class DataProcessor:
    """Handles ingestion, schema validation, frequency detection, gap filling, and stats extraction."""

    REQUIRED_COLUMNS = {"unique_id", "ds", "y"}

    @classmethod
    def load_and_validate_csv(
        cls,
        csv_bytes: bytes,
        selected_series: Optional[str] = None,
        fill_gaps: bool = True,
    ) -> Tuple[pd.DataFrame, str, List[str], str]:
        """Validates CSV format against Nixtla standards and prepares clean DataFrame.

        Returns:
            Tuple of:
            - processed DataFrame with [unique_id, ds, y]
            - active unique_id
            - list of all unique_ids in dataset
            - detected frequency string
        """
        if not csv_bytes or len(csv_bytes.strip()) == 0:
            raise DataValidationError("El archivo CSV está vacío. Por favor carga un archivo válido.")

        try:
            # Read CSV with string decoding
            content = io.BytesIO(csv_bytes)
            df = pd.read_csv(content)
        except Exception as exc:
            raise DataValidationError(f"Error al decodificar el archivo CSV: {str(exc)}") from exc

        # Column name normalization (trim whitespace & lowercase)
        column_mapping = {col: col.strip().lower() for col in df.columns}
        df.rename(columns=column_mapping, inplace=True)

        # Check required columns
        missing_cols = cls.REQUIRED_COLUMNS - set(df.columns)
        if missing_cols:
            raise DataValidationError(
                f"El archivo no contiene las columnas requeridas de Nixtla: {sorted(list(missing_cols))}. "
                f"Columnas detectadas: {list(df.columns)}. Se requiere: unique_id, ds, y"
            )

        # Filter down to required columns
        df = df[["unique_id", "ds", "y"]].copy()

        # Check for empty records
        if df.empty:
            raise DataValidationError("El archivo no contiene filas de datos.")

        # Clean unique_id
        df["unique_id"] = df["unique_id"].astype(str).str.strip()
        available_series = sorted(df["unique_id"].dropna().unique().tolist())

        if not available_series:
            raise DataValidationError("No se encontraron identificadores válidos en 'unique_id'.")

        active_series = selected_series if (selected_series and selected_series in available_series) else available_series[0]

        # Filter for active series
        df_series = df[df["unique_id"] == active_series].copy()

        # Parse and validate 'ds'
        try:
            df_series["ds"] = pd.to_datetime(df_series["ds"])
        except Exception as exc:
            raise DataValidationError(
                f"Error al convertir la columna 'ds' a formato de fecha: {str(exc)}. "
                "Asegúrate de usar formato ISO (YYYY-MM-DD o YYYY-MM-DD HH:MM:SS)."
            ) from exc

        # Drop invalid timestamps
        df_series = df_series.dropna(subset=["ds"])
        if df_series.empty:
            raise DataValidationError(f"No hay fechas válidas para la serie '{active_series}'.")

        # Sort chronologically and drop exact date duplicates (aggregate by sum or last)
        df_series = df_series.sort_values(by="ds")
        if df_series.duplicated(subset=["ds"]).any():
            # If duplicated timestamps exist for same series, sum sales (common in retail transactions)
            df_series = (
                df_series.groupby(["unique_id", "ds"], as_index=False)["y"]
                .sum()
                .sort_values(by="ds")
            )

        # Parse and validate 'y'
        df_series["y"] = pd.to_numeric(df_series["y"], errors="coerce")
        if df_series["y"].isnull().all():
            raise DataValidationError(f"La columna 'y' no contiene valores numéricos válidos en '{active_series}'.")

        # Impute single NaN values with 0 or forward fill
        df_series["y"] = df_series["y"].fillna(0.0)

        # Ensure minimum history length for neural training
        if len(df_series) < 14:
            raise DataValidationError(
                f"La serie '{active_series}' contiene {len(df_series)} puntos. "
                "Se requiere un mínimo de 14 observaciones históricas para entrenar redes neuronales."
            )

        # Detect frequency
        freq = cls.detect_frequency(df_series["ds"])

        # Handle temporal gaps if requested
        if fill_gaps and freq:
            try:
                full_date_range = pd.date_range(
                    start=df_series["ds"].min(),
                    end=df_series["ds"].max(),
                    freq=freq,
                )
                df_reindexed = pd.DataFrame({"ds": full_date_range})
                df_reindexed = pd.merge(df_reindexed, df_series, on="ds", how="left")
                df_reindexed["unique_id"] = active_series
                # Retail standard: days without sales records are filled with 0
                df_reindexed["y"] = df_reindexed["y"].fillna(0.0)
                df_series = df_reindexed
            except Exception:
                # Fallback to original series if frequency reindexing encounters non-standard intervals
                pass

        return df_series, active_series, available_series, freq or "D"

    @staticmethod
    def detect_frequency(dates: pd.Series) -> str:
        """Infers the most likely frequency of the time series."""
        inferred = pd.infer_freq(dates)
        if inferred:
            return inferred

        # If infer_freq fails due to noise, compute median difference
        if len(dates) > 2:
            diffs = dates.diff().dropna()
            median_seconds = diffs.dt.total_seconds().median()
            # Approx 1 day
            if 80000 <= median_seconds <= 90000:
                return "D"
            # Approx 1 week
            elif 590000 <= median_seconds <= 620000:
                return "W-SUN"
            # Approx 1 hour
            elif 3500 <= median_seconds <= 3700:
                return "H"
            # Approx 1 month
            elif 2400000 <= median_seconds <= 2700000:
                return "MS"

        return "D"

    @classmethod
    def calculate_statistics(
        cls,
        df_historical: pd.DataFrame,
        forecast_df: pd.DataFrame,
        unique_id: str,
        freq: str,
    ) -> SeriesDescriptiveStats:
        """Computes executive and descriptive statistics comparing historical baseline with forecast."""
        y_hist = df_historical["y"].values
        y_pred = forecast_df["y_hat"].values

        hist_mean = float(np.mean(y_hist))
        hist_std = float(np.std(y_hist))
        hist_cv = float(hist_std / hist_mean) if hist_mean > 0 else 0.0
        hist_min = float(np.min(y_hist))
        hist_max = float(np.max(y_hist))

        pred_mean = float(np.mean(y_pred))
        pred_sum = float(np.sum(y_pred))

        # Percentage change
        pct_change = (
            float(((pred_mean - hist_mean) / hist_mean) * 100.0)
            if hist_mean > 0
            else 0.0
        )

        # Trend direction classification
        if pct_change > 3.0:
            trend = "ALCISTA"
        elif pct_change < -3.0:
            trend = "BAJISTA"
        else:
            trend = "ESTABLE"

        return SeriesDescriptiveStats(
            unique_id=unique_id,
            total_historical_points=len(df_historical),
            start_date=df_historical["ds"].min().strftime("%Y-%m-%d"),
            end_date=df_historical["ds"].max().strftime("%Y-%m-%d"),
            inferred_frequency=freq,
            historical_mean=round(hist_mean, 2),
            historical_std=round(hist_std, 2),
            historical_cv=round(hist_cv, 3),
            historical_min=round(hist_min, 2),
            historical_max=round(hist_max, 2),
            forecast_mean=round(pred_mean, 2),
            forecast_sum=round(pred_sum, 2),
            percentage_change=round(pct_change, 2),
            trend_direction=trend,
        )

    @classmethod
    def to_datapoints(cls, df: pd.DataFrame) -> List[DataPoint]:
        """Converts DataFrame to list of DataPoint Pydantic models."""
        return [
            DataPoint(
                unique_id=str(row["unique_id"]),
                ds=pd.to_datetime(row["ds"]).strftime("%Y-%m-%d"),
                y=round(float(row["y"]), 2),
            )
            for _, row in df.iterrows()
        ]
