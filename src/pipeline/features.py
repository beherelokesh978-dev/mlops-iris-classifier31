
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def engineer_features():
    logging.info("Starting feature engineering")

    input_path = Path("data/processed/iris_preprocessed.csv")
    output_path = Path("data/processed/iris_features.csv")

    df = pd.read_csv(input_path)

    # Calculate sepal and petal areas
    df["sepal_area"] = (
        df["sepal length (cm)"] *
        df["sepal width (cm)"]
    )

    df["petal_area"] = (
        df["petal length (cm)"] *
        df["petal width (cm)"]
    )

    # Calculate sepal-to-petal length ratio
    df["sepal_to_petal_length_ratio"] = (
        df["sepal length (cm)"] /
        df["petal length (cm)"].replace(0, float("nan"))
    )

    # Categorize petal length
    df["petal_length_bin"] = pd.cut(
        df["petal length (cm)"],
        bins=[0, 2, 5, float("inf")],
        labels=["small", "medium", "large"],
        include_lowest=True
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    logging.info("Features saved to %s", output_path)
    logging.info("Total features: %d", len(df.columns))

if __name__ == "__main__":
    engineer_features()