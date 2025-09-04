import json
import pytest
from aceest_fitness import create_app

@pytest.fixture()
def app():
    app = create_app({"TESTING": True, "SEED_SAMPLE": True})
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_health(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "ok"

def test_index(client):
    rv = client.get("/")
    data = rv.get_json()
    assert rv.status_code == 200
    assert data["app"] == "ACEest Fitness API"
    assert "/workouts" in data["endpoints"]

def test_list_seeded_workouts(client):
    rv = client.get("/workouts")
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Seeded

def test_add_workout_success(client):
    rv = client.post("/workouts", json={"workout": "Cycling", "duration": 25})
    assert rv.status_code == 201
    assert rv.get_json()["message"] == "Workout added."

@pytest.mark.parametrize(
    "payload,expected_status",
    [
        ({}, 400),
        ({"workout": ""}, 400),
        ({"workout": "Run"}, 400),
        ({"workout": "Run", "duration": 0}, 400),
        ({"workout": "Run", "duration": -3}, 400),
        ({"workout": "Run", "duration": "ten"}, 400),
    ],
)
def test_add_workout_validation(client, payload, expected_status):
    rv = client.post("/workouts", json=payload)
    assert rv.status_code == expected_status
