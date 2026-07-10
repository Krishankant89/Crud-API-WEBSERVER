FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=5000 \
    DATABASE_URL=sqlite:///students.db

WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /opt/venv /opt/venv
COPY app ./app
COPY run.py .
COPY migrations ./migrations

RUN mkdir -p /app/instance && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["sh", "-c", "gunicorn --workers 2 --bind 0.0.0.0:${PORT} run:app"]
