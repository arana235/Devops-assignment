# ACEest Fitness & Gym — DevOps Assignment (Flask + Pytest + Docker + GitHub Actions)

This repository contains a minimal Flask API for a fictional fitness app, fully wired with tests, containerization, and CI/CD using GitHub Actions.

## Features
- Flask app with endpoints:
  - `GET /health` — health check
  - `GET /` — API info
  - `GET /workouts` — list all workouts (in-memory)
  - `POST /workouts` — add a workout: `{ "workout": "Running", "duration": 30 }`
- Pytest unit tests covering happy-path and validation cases
- Multi-stage Dockerfile:
  - **test** stage runs `pytest` inside the container
  - **runtime** stage serves the app with Gunicorn on port `8000`
- GitHub Actions workflow to:
  - Install deps & run tests on the host
  - Build production Docker image
  - Build **test** image and run tests inside the container

## Local Development

### 1) Set up & run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=wsgi:app   # Windows (PowerShell): $env:FLASK_APP="wsgi:app"
flask run -p 8000
```
Visit http://127.0.0.1:8000/health

### 2) Run tests
```bash
pytest
```

## Docker

### Build & run production image
```bash
docker build -t aceest-fitness:latest .
docker run --rm -p 8000:8000 aceest-fitness:latest
# Then: http://127.0.0.1:8000/health
```

### Run tests inside container
```bash
docker build --target test -t aceest-fitness-test .
docker run --rm aceest-fitness-test
```

## GitHub Actions CI/CD
The workflow file is at `.github/workflows/ci.yml` and triggers on every push and pull request. It runs unit tests on the host, builds the production Docker image, and executes tests **inside the Docker image** using the `test` stage.

## Notes
- The app uses an in-memory list for workouts to keep the scope minimal for the assignment.
- For a real deployment, add persistence and secure configuration.
