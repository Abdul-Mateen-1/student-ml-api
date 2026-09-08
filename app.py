"""HTTP API for the student ML inference service."""

from math import isfinite
from pathlib import Path

from flask import Flask, jsonify, request


MODEL_VERSION = "model-1"


def read_application_version() -> str:
    """Return the source-controlled application version."""
    return Path(__file__).with_name("VERSION").read_text(encoding="utf-8").strip()


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(
            status="healthy",
            application="student-ml-api",
            application_version=read_application_version(),
            model_version=MODEL_VERSION,
        )

    @app.post("/predict")
    def predict():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="Request body must be a valid JSON object"), 400

        if "value" not in payload:
            return jsonify(error="Missing required field: value"), 400

        value = payload["value"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return jsonify(error="Field 'value' must be a number"), 400
        if not isfinite(value):
            return jsonify(error="Field 'value' must be a finite number"), 400

        return jsonify(input=value, prediction=value * 2)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
