# ==============================================================================
# Multi-Stage / Lean Production Dockerfile for Render Deployment
# Python 3.11 Slim with PyTorch CPU optimization & Non-Root Security
# ==============================================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install essential system dependencies (curl for healthchecks, minimal build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create a non-root user and group for security compliance
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Upgrade pip and install CPU-only PyTorch to prevent huge CUDA bloat on Render
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Copy and install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and sample data
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser data/ ./data/

# Switch to non-root user
USER appuser

# Expose Render default port
EXPOSE 8000

# Healthcheck probe for container orchestrators
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Launch production server with dynamic port binding for Render
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
