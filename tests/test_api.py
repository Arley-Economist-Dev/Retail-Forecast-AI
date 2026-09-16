"""Integration tests for FastAPI endpoints and forecasting workflows."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Ensure healthcheck endpoint returns healthy status and system parameters."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert data["cpu_mode"] is True


def test_sample_data_endpoint():
    """Ensure sample CSV is served correctly with proper media type."""
    response = client.get("/api/v1/sample-data")
    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    assert "unique_id,ds,y" in response.text


def test_models_endpoint():
    """Ensure available models endpoint returns supported architectures."""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    model_ids = [m["id"] for m in data["models"]]
    assert "NHITS" in model_ids
    assert "NBEATS" in model_ids


def test_forecast_invalid_csv_schema():
    """Ensure invalid CSV payload returns 422 Unprocessable Entity."""
    bad_csv = b"col1,col2\nval1,val2"
    response = client.post(
        "/api/v1/forecast",
        files={"file": ("bad.csv", bad_csv, "text/csv")},
        data={"horizon": 7, "model": "NHITS"},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert data["error_type"] == "DataValidationError"


def test_forecast_successful_execution():
    """Verify end-to-end forecast request with valid data returns 200 and complete schema."""
    valid_csv = b"""unique_id,ds,y
STORE_01,2025-01-01,100
STORE_01,2025-01-02,110
STORE_01,2025-01-03,105
STORE_01,2025-01-04,120
STORE_01,2025-01-05,130
STORE_01,2025-01-06,115
STORE_01,2025-01-07,125
STORE_01,2025-01-08,105
STORE_01,2025-01-09,112
STORE_01,2025-01-10,122
STORE_01,2025-01-11,135
STORE_01,2025-01-12,140
STORE_01,2025-01-13,118
STORE_01,2025-01-14,128
"""
    response = client.post(
        "/api/v1/forecast",
        files={"file": ("test.csv", valid_csv, "text/csv")},
        data={"horizon": 5, "model": "NHITS"},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["model_used"] == "NHITS"
    assert data["horizon"] == 5
    assert data["series_id"] == "STORE_01"
    assert len(data["forecast"]) == 5
    assert len(data["historical"]) == 14
    assert "statistics" in data
    assert "executive_summary_markdown" in data
    assert "Demand & Trend Diagnostics" in data["executive_summary_markdown"]
    assert data["execution_time_seconds"] > 0


def test_forecast_language_selection_spanish():
    """Verify that specifying lang='es' returns executive summary in Spanish."""
    valid_csv = b"""unique_id,ds,y
STORE_01,2025-01-01,100
STORE_01,2025-01-02,110
STORE_01,2025-01-03,105
STORE_01,2025-01-04,120
STORE_01,2025-01-05,130
STORE_01,2025-01-06,115
STORE_01,2025-01-07,125
STORE_01,2025-01-08,105
STORE_01,2025-01-09,112
STORE_01,2025-01-10,122
STORE_01,2025-01-11,135
STORE_01,2025-01-12,140
STORE_01,2025-01-13,118
STORE_01,2025-01-14,128
"""
    response = client.post(
        "/api/v1/forecast",
        files={"file": ("test.csv", valid_csv, "text/csv")},
        data={"horizon": 5, "model": "NHITS", "lang": "es"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "Diagnóstico de Demanda y Tendencia" in data["executive_summary_markdown"]

