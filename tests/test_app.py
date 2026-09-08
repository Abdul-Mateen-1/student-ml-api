"""Unit tests for the prediction API."""

import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "wrong",
        "application": "student-ml-api",
        "version": "1.0.0",
    }


def test_predict_success(client):
    response = client.post("/predict", json={"value": 10})

    assert response.status_code == 200
    assert response.get_json() == {"input": 10, "prediction": 20}


def test_predict_accepts_floating_point_value(client):
    response = client.post("/predict", json={"value": 2.5})

    assert response.status_code == 200
    assert response.get_json() == {"input": 2.5, "prediction": 5.0}


def test_predict_rejects_missing_value(client):
    response = client.post("/predict", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required field: value"}


@pytest.mark.parametrize("invalid_value", ["ten", None, True])
def test_predict_rejects_non_numeric_value(client, invalid_value):
    response = client.post("/predict", json={"value": invalid_value})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Field 'value' must be a number"}


def test_predict_rejects_invalid_json(client):
    response = client.post(
        "/predict", data="not-json", content_type="application/json"
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Request body must be a valid JSON object"}
