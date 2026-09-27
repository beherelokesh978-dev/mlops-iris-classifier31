
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def preprocess_data():
    logging.info("Starting data preprocessing")

    input_path = Path("data/raw/iris_raw.csv")
    output_path = Path("data/processed/iris_preprocessed.csv")

    df = pd.read_csv(input_path)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert measurement columns to numeric
    numeric_columns = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    # Fill missing numeric values with the median
    for column in numeric_columns:
        df[column] = df[column].fillna(
            df[column].median()
        )

    # Remove rows with missing species
    df = df.dropna(subset=["species"])

    # Remove collection timestamp
    df = df.drop(columns=["collected_at"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    logging.info("Preprocessed data saved to %s", output_path)
    logging.info("Remaining rows: %d", len(df))

if __name__ == "__main__":
    preprocess_data()