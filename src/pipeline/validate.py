
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

EXPECTED_COLUMNS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "species",
    "sepal_area",
    "petal_area",
    "sepal_to_petal_length_ratio",
    "petal_length_bin",
]

ALLOWED_SPECIES = {"setosa", "versicolor", "virginica"}


class DataValidationError(ValueError):
    """Raised when the input dataset fails validation."""


def validate(input_path="data/processed/iris_features.csv"):
    """Validate an Iris feature dataset and return the DataFrame."""
    logging.info("Starting data validation")

    input_path = Path(input_path)
    df = pd.read_csv(input_path)

    errors = []

    # Check required columns
    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]
    if missing_columns:
        raise DataValidationError(
            f"Missing expected columns: {missing_columns}"
        )

    # Check for unexpected column names or ordering
    if list(df.columns) != EXPECTED_COLUMNS:
        errors.append("Column names or order are incorrect")

    # Check missing values
    if df.isnull().any().any():
        errors.append("Missing values found in the dataset")

    # Check species names
    if not set(df["species"].unique()).issubset(ALLOWED_SPECIES):
        errors.append("Unexpected species values")

    # Check measurement ranges
    ranges = {
        "sepal length (cm)": (3.0, 9.0),
        "sepal width (cm)": (0.0, 10.0),
        "petal length (cm)": (0.0, 10.0),
        "petal width (cm)": (0.0, 10.0),
    }

    for column, (minimum, maximum) in ranges.items():
        if not df[column].between(minimum, maximum).all():
            errors.append(f"Values out of expected range in {column}")

    if errors:
        raise DataValidationError(
            f"Validation failed with {len(errors)} error(s): "
            + "; ".join(errors)
        )

    logging.info("Data validation successful")
    logging.info("Validated %d rows", len(df))

    return df


def validate_data():
    """Keep compatibility with the original practical."""
    return validate()


if __name__ == "__main__":
    try:
        validate_data()
    except Exception as error:
        logging.error("Validation failed: %s", error)
        raise SystemExit(1)
