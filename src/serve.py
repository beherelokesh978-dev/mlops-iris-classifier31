"""HTTP API for the containerized Iris classifier."""

import json
import logging
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

import joblib
import pandas as pd

MODEL_PATH = Path("models/final_model.joblib")
ENCODER_PATH = Path("models/label_encoder.joblib")
FEATURE_ORDER = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "sepal_area",
    "petal_area",
    "sepal_to_petal_length_ratio",
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class PredictionHandler(BaseHTTPRequestHandler):
    model = None
    label_encoder = None

    def _respond(self, status, payload):
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        if urlsplit(self.path).path == "/health":
            self._respond(200, {"status": "healthy"})
            return
        self._respond(404, {"error": "not found"})

    def do_POST(self):
        if urlsplit(self.path).path != "/predict":
            self._respond(404, {"error": "not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length < 0:
                raise ValueError("Content-Length must not be negative")
            body = json.loads(self.rfile.read(content_length))
            if not isinstance(body, dict):
                self._respond(400, {"error": "JSON body must be an object"})
                return

            missing = [name for name in FEATURE_ORDER if name not in body]
            if missing:
                self._respond(
                    400,
                    {"error": "Missing features", "missing": missing},
                )
                return

            features = [float(body[name]) for name in FEATURE_ORDER]
            if not all(math.isfinite(value) for value in features):
                raise ValueError("Feature values must be finite numbers")
        except (json.JSONDecodeError, TypeError, ValueError):
            self._respond(400, {"error": "Invalid JSON or feature values"})
            return

        feature_array = pd.DataFrame([features], columns=FEATURE_ORDER)
        prediction_index = self.model.predict(feature_array)[0]
        prediction = self.label_encoder.inverse_transform([prediction_index])[0]
        probabilities = self.model.predict_proba(feature_array)[0].tolist()
        self._respond(
            200,
            {
                "prediction": prediction,
                "probabilities": probabilities,
            },
        )


def main():
    PredictionHandler.model = joblib.load(MODEL_PATH)
    PredictionHandler.label_encoder = joblib.load(ENCODER_PATH)

    with ThreadingHTTPServer(("0.0.0.0", 8000), PredictionHandler) as server:
        logging.info("Serving model on http://0.0.0.0:8000")
        server.serve_forever()


if __name__ == "__main__":
    main()
