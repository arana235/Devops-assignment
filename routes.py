from flask import Blueprint, current_app, request, jsonify

bp = Blueprint("api", __name__)

@bp.get("/workouts")
def list_workouts():
    return jsonify(current_app.workouts), 200

@bp.post("/workouts")
def add_workout():
    data = request.get_json(silent=True) or {}
    workout = (data.get("workout") or "").strip()
    duration = data.get("duration")

    # Validate payload
    if not workout:
        return {"error": "Field 'workout' is required."}, 400
    try:
        duration = int(duration)
    except (TypeError, ValueError):
        return {"error": "Field 'duration' must be an integer (minutes)."}, 400
    if duration <= 0:
        return {"error": "Field 'duration' must be positive."}, 400

    current_app.workouts.append({"workout": workout, "duration": duration})
    return {"message": "Workout added.", "count": len(current_app.workouts)}, 201
