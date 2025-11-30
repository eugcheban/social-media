# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files & force unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry directly (no pipx)
ENV POETRY_VERSION=2.2.1
RUN pip install "poetry==$POETRY_VERSION"

# Set up working directory
WORKDIR /backend

# Copy dependency files first for layer caching
COPY backend/pyproject.toml backend/poetry.lock* ./

# Configure Poetry (disable virtualenv creation in Docker)
RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-root

# Default command
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
