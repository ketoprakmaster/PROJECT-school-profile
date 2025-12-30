# ---------------------------
# Stage 1: Build frontend assets
# ---------------------------
FROM node:24-slim AS frontend-builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci  # Faster, cleaner install than 'npm install'
COPY ./src/ /app/src/

RUN npm run build:css

# ---------------------------
# Stage 2: Build Python environment
# ---------------------------
FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder-python

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies only
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Prune the venv: Remove caches, tests, and documentation
RUN find /app/.venv -type d -name "__pycache__" -prune -exec rm -rf {} + \
 && find /app/.venv -type f -name "*.pyc" -delete \
 && find /app/.venv -type f -name "*.pyo" -delete


# ---------------------------
# Stage 3: Final production image
# ---------------------------
FROM python:3.14-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy venv and assets
COPY --from=builder-python /app/.venv /opt/venv
COPY --from=frontend-builder /app/src/themes/static/ /app/src/themes/static/

# Copy only the necessary source code (ignore tests/docs if possible)
COPY ./src/ /app/src/
COPY --chmod=755 ./docker/run.sh /app/run.sh

# Create media/static folders and set permissions
RUN mkdir -p /app/src/media /app/src/static && \
    chmod -R 777 /app/src/media

WORKDIR /app/src
EXPOSE 8000

ENTRYPOINT ["/app/run.sh"]
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "-w", "4"]
