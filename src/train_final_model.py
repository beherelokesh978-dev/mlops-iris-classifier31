"""Train and save the Iris classifier for container deployment."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

DATA_PATH = Path("data/processed/iris_features.csv")
MODEL_DIR = Path("models")
FEATURE_COLS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "sepal_area",
    "petal_area",
    "sepal_to_petal_length_ratio",
]


def main():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURE_COLS].copy()
    X = X.fillna(X.median())

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["species"])

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42,
    )
    model.fit(X, y)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_DIR / "final_model.joblib")
    joblib.dump(label_encoder, MODEL_DIR / "label_encoder.joblib")

    print(f"Trained model using {len(df)} rows.")
    print(f"Classes: {list(label_encoder.classes_)}")


if __name__ == "__main__":
    main()
