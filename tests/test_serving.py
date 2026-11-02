"""Tests for the containerized model's HTTP endpoints."""

import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import numpy as np
import pytest

from src.serve import FEATURE_ORDER, PredictionHandler


class StubModel:
    def predict(self, features):
        return np.array([0])

    def predict_proba(self, features):
        return np.array([[0.8, 0.1, 0.1]])


class StubLabelEncoder:
    def inverse_transform(self, values):
        return np.array(["setosa"])


@pytest.fixture
def api_url():
    PredictionHandler.model = StubModel()
    PredictionHandler.label_encoder = StubLabelEncoder()
    server = ThreadingHTTPServer(("127.0.0.1", 0), PredictionHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{server.server_port}"

    server.shutdown()
    server.server_close()
    thread.join()
    PredictionHandler.model = None
    PredictionHandler.label_encoder = None


def test_health_endpoint_returns_healthy(api_url):
    with urlopen(f"{api_url}/health") as response:
        assert response.status == 200
        assert json.load(response) == {"status": "healthy"}


def test_prediction_endpoint_returns_species_and_probabilities(api_url):
    payload = {feature: 1.0 for feature in FEATURE_ORDER}
    request = Request(
        f"{api_url}/predict",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request) as response:
        result = json.load(response)

    assert result == {
        "prediction": "setosa",
        "probabilities": [0.8, 0.1, 0.1],
    }


def test_prediction_endpoint_reports_missing_features(api_url):
    request = Request(
        f"{api_url}/predict",
        data=json.dumps({"sepal length (cm)": 5.1}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with pytest.raises(HTTPError) as error:
        urlopen(request)

    assert error.value.code == 400
    result = json.load(error.value)
    assert result["error"] == "Missing features"
    assert len(result["missing"]) == len(FEATURE_ORDER) - 1


def test_prediction_endpoint_rejects_non_finite_features(api_url):
    payload = {feature: 1.0 for feature in FEATURE_ORDER}
    payload["sepal length (cm)"] = float("nan")
    request = Request(
        f"{api_url}/predict",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with pytest.raises(HTTPError) as error:
        urlopen(request)

    assert error.value.code == 400
    assert json.load(error.value) == {
        "error": "Invalid JSON or feature values"
    }
