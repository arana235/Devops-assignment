# syntax=docker/dockerfile:1

# Base image
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Test stage - runs pytest inside the image
FROM base AS test
COPY . /app
# default command for the test image
CMD ["pytest"]

# Production runtime image
FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=base /usr/local /usr/local
COPY aceest_fitness /app/aceest_fitness
COPY wsgi.py /app/wsgi.py
EXPOSE 8000
# Gunicorn WSGI server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
