"""Application configuration and environment variables management using Pydantic Settings."""

from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General Project Info
    PROJECT_NAME: str = "Retail Demand Forecasting & AI Analyst"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Forecasting Engine Configuration (CPU & Render optimized)
    DEFAULT_HORIZON: int = 14
    MAX_HORIZON: int = 90
    DEFAULT_MODEL: Literal["NHITS", "NBEATS"] = "NHITS"
    MAX_EPOCHS_OR_STEPS: int = 60
    BATCH_SIZE: int = 32

    # LLM Settings (Supports Gemini & Groq with free tiers)
    LLM_PROVIDER: Literal["gemini", "groq", "auto", "heuristic"] = "auto"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-3.6-flash"
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.1-70b-versatile"

    # Upload Constraints
    MAX_UPLOAD_SIZE_MB: int = 20


settings = Settings()
