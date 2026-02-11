import os
from flask import Flask, render_template, jsonify
from pathlib import Path
import json

app = Flask(__name__)

def load_exercises():
    json_path = Path(__file__).parent.parent / "data" / "exercise_json" / "parsed_exercises.json"
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    exercises = load_exercises()
    return render_template("index.html", exercises=exercises)

@app.route("/exercise/<exercise_name>")
def exercise_detail(exercise_name):
    exercises = load_exercises()
    exercise_data = exercises.get(exercise_name, {})
    return render_template("exercise.html", exercise_name=exercise_name, exercise_data=exercise_data)

@app.route("/api/exercises")
def api_exercises():
    return jsonify(load_exercises())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)