"""FastAPI entrypoint for the Retail Time Series Forecasting application."""

import logging
import os
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.schemas.forecast import ForecastResponse, HealthResponse, SeriesDescriptiveStats
from app.services.data_processor import DataProcessor, DataValidationError
from app.services.forecaster import ForecasterService
from app.services.llm_analyst import LLMAnalystService

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
)
logger = logging.getLogger("retail_forecaster")

# FastAPI App Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-grade retail time series forecasting with Nixtla NeuralForecast, CPU optimization and LLM strategic analyst.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR.parent / "data"

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.exception_handler(DataValidationError)
async def data_validation_exception_handler(request: Request, exc: DataValidationError):
    """Handles time series contract validation failures with 422 Unprocessable Entity."""
    logger.warning(f"Data validation failed: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": "error", "error_type": "DataValidationError", "detail": str(exc)},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catches unhandled server exceptions and returns standard JSON error."""
    logger.error(f"Unhandled server exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error_type": "InternalServerError",
            "detail": "Ha ocurrido un error inesperado al procesar la solicitud.",
        },
    )


@app.get("/", include_in_schema=False)
async def root_view():
    """Serves the frontend single-page dashboard."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Retail Time Series Forecasting API is running. Visit /docs for OpenAPI specs."}


@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
async def healthcheck():
    """Healthcheck endpoint for Render container health probes and uptime monitoring."""
    active_provider = "gemini" if settings.GEMINI_API_KEY else ("groq" if settings.GROQ_API_KEY else "heuristic")
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        environment=os.getenv("RENDER_ENV", "production" if not settings.DEBUG else "development"),
        llm_provider=active_provider,
        cpu_mode=True,
    )


@app.get("/api/v1/sample-data", tags=["Data"])
async def get_sample_data():
    """Returns the bundled sample retail sales CSV for instant zero-friction demonstrations."""
    sample_file = DATA_DIR / "sample_retail_sales.csv"
    if not sample_file.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El archivo de datos de muestra no se encuentra disponible.",
        )
    return FileResponse(
        sample_file,
        media_type="text/csv",
        filename="sample_retail_sales.csv",
    )


@app.get("/api/v1/models", tags=["Forecasting"])
async def get_available_models():
    """Returns the available neural network architectures and descriptions."""
    return {
        "models": [
            {
                "id": "NHITS",
                "name": "NHITS (Neural Hierarchical Interpolation)",
                "description": "Excelente para series con múltiples frecuencias y patrones de estacionalidad. Rápido y eficiente en CPU.",
                "recommended": True,
            },
            {
                "id": "NBEATS",
                "name": "NBEATS (Neural Basis Expansion Analysis)",
                "description": "Descomposición neuronal profunda en componentes de tendencia y estacionalidad.",
                "recommended": False,
            },
        ]
    }


@app.post("/api/v1/forecast", response_model=ForecastResponse, tags=["Forecasting"])
async def generate_forecast(
    file: UploadFile = File(..., description="CSV con columnas requeridas: unique_id, ds, y"),
    horizon: int = Form(14, ge=1, le=90, description="Horizonte de pronóstico a predecir"),
    model: str = Form("NHITS", description="Arquitectura neuronal: NHITS o NBEATS"),
    selected_series: Optional[str] = Form(None, description="Identificador único (unique_id) a procesar"),
    fill_gaps: bool = Form(True, description="Rellenar vacíos temporales con ceros"),
    lang: str = Form("en", description="Language for executive briefing: 'en' or 'es'"),
):
    """Processes uploaded time series CSV, executes NeuralForecast on CPU, and synthesizes LLM executive insights."""
    start_time = time.time()

    # Read uploaded file content
    try:
        csv_bytes = await file.read()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo leer el archivo cargado: {str(exc)}",
        ) from exc

    # Validate file size
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(csv_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"El archivo excede el tamaño máximo permitido de {settings.MAX_UPLOAD_SIZE_MB}MB.",
        )

    # 1. Ingestion & Contract Validation
    df_clean, active_series, available_series, freq = DataProcessor.load_and_validate_csv(
        csv_bytes=csv_bytes,
        selected_series=selected_series,
        fill_gaps=fill_gaps,
    )

    # 2. Neural Forecasting Pipeline (CPU optimized)
    preds_df, forecast_points = ForecasterService.run_forecast(
        df_clean=df_clean,
        horizon=horizon,
        model_name=model,
        freq=freq,
    )

    # 3. Descriptive and Trend Statistical Summary
    stats = DataProcessor.calculate_statistics(
        df_historical=df_clean,
        forecast_df=preds_df,
        unique_id=active_series,
        freq=freq,
    )

    # 4. Strategic Executive Report Generation via LLM (Pre-generate both languages for instant UI switching)
    report_active = LLMAnalystService.generate_executive_briefing(
        stats=stats,
        horizon=horizon,
        model_used=model,
        lang=lang,
    )
    alt_lang = "es" if lang.lower() == "en" else "en"
    report_alt = LLMAnalystService.generate_executive_briefing(
        stats=stats,
        horizon=horizon,
        model_used=model,
        lang=alt_lang,
    )
    executive_reports = {
        lang.lower(): report_active,
        alt_lang: report_alt,
    }

    # 5. Format historical datapoints for chart rendering
    historical_points = DataProcessor.to_datapoints(df_clean)

    elapsed_time = round(time.time() - start_time, 2)
    logger.info(
        f"Forecast completed for series='{active_series}' with model='{model}', "
        f"horizon={horizon}, latency={elapsed_time}s"
    )

    return ForecastResponse(
        status="success",
        model_used=model.upper(),
        horizon=horizon,
        series_id=active_series,
        available_series=available_series,
        historical=historical_points,
        forecast=forecast_points,
        statistics=stats,
        executive_summary_markdown=report_active,
        executive_reports=executive_reports,
        execution_time_seconds=elapsed_time,
    )


@app.post("/api/v1/interpret", tags=["Forecasting"])
async def re_interpret_forecast(
    stats: SeriesDescriptiveStats,
    horizon: int = 14,
    model: str = "NHITS",
    lang: str = "en",
):
    """Generates an executive report on-the-fly for existing forecast stats in the specified language."""
    report = LLMAnalystService.generate_executive_briefing(
        stats=stats,
        horizon=horizon,
        model_used=model,
        lang=lang,
    )
    return {
        "status": "success",
        "lang": lang,
        "executive_summary_markdown": report,
    }
