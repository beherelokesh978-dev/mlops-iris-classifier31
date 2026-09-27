
import logging
import sys
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def validate_data():
    logging.info("Starting data validation")

    input_path = Path("data/processed/iris_features.csv")
    df = pd.read_csv(input_path)

    expected_columns = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
        "species",
        "sepal_area",
        "petal_area",
        "sepal_to_petal_length_ratio",
        "petal_length_bin"
    ]

    # Check the schema
    if list(df.columns) != expected_columns:
        raise ValueError("Column names or order are incorrect")

    # Check for missing values
    if df.isnull().any().any():
        raise ValueError("Missing values found in the dataset")

    # Check allowed species
    allowed_species = {
        "setosa", "versicolor", "virginica"
    }
    if not set(df["species"].unique()).issubset(allowed_species):
        raise ValueError("Invalid species found")

    # Check measurement ranges
    ranges = {
        "sepal length (cm)": (0, 10),
        "sepal width (cm)": (0, 10),
        "petal length (cm)": (0, 10),
        "petal width (cm)": (0, 10)
    }

    for column, (minimum, maximum) in ranges.items():
        if not df[column].between(minimum, maximum).all():
            raise ValueError(
                f"Values out of range in {column}"
            )

    logging.info("Data validation successful")
    logging.info("Validated %d rows", len(df))

if __name__ == "__main__":
    try:
        validate_data()
    except Exception as error:
        logging.error("Validation failed: %s", error)
        sys.exit(1)