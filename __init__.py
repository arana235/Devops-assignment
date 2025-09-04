from flask import Flask
from typing import Optional, Dict

def create_app(test_config: Optional[Dict] = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev")

    # In-memory "database"
    app.workouts = []

    @app.get("/health")
    def health() -> tuple[dict, int]:
        return {"status": "ok"}, 200

    @app.get("/")
    def index() -> tuple[dict, int]:
        return {
            "app": "ACEest Fitness API",
            "message": "Welcome to ACEest Fitness & Gym",
            "endpoints": ["/health", "/workouts"],
        }, 200

    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    # Optional: preload some sample data in testing
    if test_config and test_config.get("SEED_SAMPLE"):
        app.workouts.extend([
            {"workout": "Push Ups", "duration": 10},
            {"workout": "Running", "duration": 30},
        ])

    return app
