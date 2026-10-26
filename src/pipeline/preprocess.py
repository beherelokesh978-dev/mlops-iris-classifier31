
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

NUMERIC_COLUMNS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
]


def preprocess(
    input_path="data/raw/iris_raw.csv",
    output_path="data/processed/iris_preprocessed.csv",
):
    """Clean Iris data and save the processed dataset."""
    logging.info("Starting data preprocessing")

    input_path = Path(input_path)
    output_path = Path(output_path)

    df = pd.read_csv(input_path)

    # Remove duplicate rows
    df = df.drop_duplicates().copy()

    # Remove rows without a target label
    if "species" in df.columns:
        df = df.dropna(subset=["species"])

    # Convert measurements to numeric and fill missing values
    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column], errors="coerce"
            )

            if not df.empty:
                median_value = df[column].median()
                df[column] = df[column].fillna(median_value)

    # Remove timestamp if present
    if "collected_at" in df.columns:
        df = df.drop(columns=["collected_at"])

    # Save the processed data
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    logging.info("Preprocessed data saved to %s", output_path)
    logging.info("Remaining rows: %d", len(df))

    return df


def preprocess_data():
    """Keep compatibility with the original practical."""
    return preprocess()


if __name__ == "__main__":
    preprocess_data()
