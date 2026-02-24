# syntax=docker/dockerfile:1

# ============================================
# Stage 1: Build Dependencies
# ============================================
FROM python:3.14-slim AS builder

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================
# Stage 2: Production Runtime
# ============================================
FROM python:3.14-slim AS production

ARG APP_VERSION=dev
ARG BUILD_DATE

LABEL org.opencontainers.image.title="Bem Saúde API" \
      org.opencontainers.image.description="FastAPI backend for Bem Saúde" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      maintainer="Bem Saúde"

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

WORKDIR /app

# Copy source code
COPY src/ .

# Create non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "bem_saude.principal:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
