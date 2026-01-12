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

# Set up working directory
WORKDIR /backend

# Copy dependency files first for layer caching
COPY backend/pyproject.toml backend/poetry.lock* ./

# Install poetry
RUN pip install "poetry==1.8.2"

# Configure Poetry (disable virtualenv creation in Docker)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Run migrations and start server
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
