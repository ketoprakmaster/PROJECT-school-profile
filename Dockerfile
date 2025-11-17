# Stage 1: Build frontend assets
FROM node:24-slim AS frontend-builder

WORKDIR /app

# copy the entire wagtail project source
COPY ./src/ /app/src

# Copy package files and install ALL dependencies needed for the build (including dev deps like Tailwind)
COPY package.json package-lock.json* ./
RUN npm install


# Copy frontend source files (the input CSS files)
COPY ./src/themes/source/ /app/src/themes/source/

# Build CSS (Templates are now available at /app/src/ for the build tool to scan)
RUN npm run build:css


# Stage 2: Build Python dependencies
FROM python:3.14-slim-bookworm AS python-builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install uv (The dependency installer)
RUN pip install uv

WORKDIR /app

# Create and activate virtual environment
# We create the venv outside of the standard working directory to isolate it
RUN python -m venv /opt/venv

# Set the PATH environment variable to include the venv's bin directory
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies into the virtual environment
COPY requirements.txt /tmp/requirements.txt
# We use the 'uv' installed in the base image, but it installs into the venv
RUN uv pip install --no-cache-dir -r /tmp/requirements.txt


# Final stage: Production image
# Use a lean base image for the final deployable artifact
FROM python:3.14-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=core.settings.production

WORKDIR /app

# Copy virtual environment from python-builder
COPY --from=python-builder /opt/venv /opt/venv

# Copy built frontend assets
# Note: Ensure the destination path matches where Django expects it, typically /app/src/static or similar
COPY --from=frontend-builder /app/src/themes/static/css/styles.css /app/src/themes/static/css/styles.css

# Copy application code (Only the necessary files, excluding the ones already in the build stage)
COPY src/ /app/src/

# Set the working directory to the Django project root
WORKDIR /app/src

# Collect static files
# Explicitly call the Python interpreter from the virtual environment (venv)
RUN /opt/venv/bin/python manage.py collectstatic --noinput -v 3

# Expose port 8000
EXPOSE 8000

# Run gunicorn
# Use the executable directly from the venv's bin folder
CMD ["/opt/venv/bin/gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
