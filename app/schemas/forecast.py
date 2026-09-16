"""Pydantic schemas for forecasting request validation and response formatting."""

from typing import List, Optional
from pydantic import BaseModel, Field


class DataPoint(BaseModel):
    """Represents a single historical time series observation."""

    unique_id: str = Field(..., description="Entity or SKU identifier")
    ds: str = Field(..., description="Timestamp in ISO or standard date format")
    y: float = Field(..., description="Observed numeric value (e.g. sales units or revenue)")


class ForecastPoint(BaseModel):
    """Represents a single forecasted data point."""

    unique_id: str = Field(..., description="Entity or SKU identifier")
    ds: str = Field(..., description="Forecasted future timestamp")
    y_hat: float = Field(..., description="Predicted expected value")
    y_hat_lower: Optional[float] = Field(None, description="Lower prediction interval bound")
    y_hat_upper: Optional[float] = Field(None, description="Upper prediction interval bound")


class SeriesDescriptiveStats(BaseModel):
    """Statistical summary of the time series for MLOps diagnostics and LLM briefing."""

    unique_id: str
    total_historical_points: int
    start_date: str
    end_date: str
    inferred_frequency: str
    historical_mean: float
    historical_std: float
    historical_cv: float = Field(..., description="Coefficient of Variation (std / mean)")
    historical_min: float
    historical_max: float
    forecast_mean: float
    forecast_sum: float
    percentage_change: float = Field(..., description="Projected delta vs historical baseline")
    trend_direction: str = Field(..., description="Categorical trend: ALCISTA, BAJISTA, ESTABLE")


class ForecastResponse(BaseModel):
    """Unified response schema for the forecasting endpoint."""

    status: str = Field("success", description="Execution status code")
    model_used: str = Field(..., description="Architecture used: NHITS or NBEATS")
    horizon: int = Field(..., description="Forecasting horizon steps")
    series_id: str = Field(..., description="Current displayed unique_id")
    available_series: List[str] = Field(default_factory=list, description="All series found in CSV")
    historical: List[DataPoint] = Field(..., description="Validated historical observations")
    forecast: List[ForecastPoint] = Field(..., description="Model predictions")
    statistics: SeriesDescriptiveStats = Field(..., description="Descriptive and trend statistics")
    executive_summary_markdown: str = Field(..., description="LLM generated strategic retail report")
    executive_reports: dict[str, str] = Field(
        default_factory=dict,
        description="Multilingual executive summaries keyed by language code: {'en': '...', 'es': '...'}",
    )
    execution_time_seconds: float = Field(..., description="Total pipeline execution latency in seconds")


class HealthResponse(BaseModel):
    """Healthcheck response model for container orchestration and uptime monitors."""

    status: str = "healthy"
    version: str
    environment: str
    llm_provider: str
    cpu_mode: bool = True
