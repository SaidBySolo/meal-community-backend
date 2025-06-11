# Build Stage
FROM python:3.13-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main && \
    ls -la /app && \
    ls -la /app/.venv && \
    rm -rf $POETRY_CACHE_DIR


# Production Stage
FROM python:3.13-slim as production

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY backend/ ./backend/
COPY README.md .

RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["python", "-m", "backend", "--host", "0.0.0.0", "--port", "8000"]