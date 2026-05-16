FROM python:3.12-slim AS builder

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.12-slim AS production

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup scripts/ ./scripts/
COPY --chown=appuser:appgroup alembic.ini ./
COPY --chown=appuser:appgroup pyproject.toml ./

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app"

USER appuser

EXPOSE ${APP_PORT}

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${APP_PORT}/health')" || exit 1

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT} --workers 4"]
