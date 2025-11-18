# ---------------------------
# Stage 1: Build frontend assets (Tailwind)
# ---------------------------
FROM node:24-slim AS frontend-builder

WORKDIR /app

# Install frontend deps
COPY package.json package-lock.json* ./
RUN npm install

# Copy only the files needed for CSS build
COPY ./src/themes/source/ /app/src/themes/source/
COPY ./src/ /app/src/

# Build CSS
RUN npm run build:css



# ---------------------------
# Stage 2: Build Python dependencies using uv
# ---------------------------
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder-python

# Install the project into `/app`
WORKDIR /app

# Ensure installed tools can be executed out of the box
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Enable bytecode compilation
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev 



# ---------------------------
# Stage 3: Final production image
# ---------------------------
FROM python:3.14-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/venv/bin:$PATH"

WORKDIR /app

# Copy virtual environment
COPY --from=builder-python /app/.venv /venv
# Copy built frontend assets
COPY --from=frontend-builder /app/src/themes/static/ /app/src/themes/static/
# Copy Django project
COPY ./src/ /app/src/

# Copy startup script (Linux LF only)
COPY --chmod=755 ./docker/run.sh /app/run.sh

# Create media directory
RUN mkdir -p /app/src/media && \
    chmod -R 777 /app/src/media

WORKDIR /app/src

EXPOSE 8000

CMD ["/app/run.sh"]
