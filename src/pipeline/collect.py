
import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_iris

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def collect_data():
    logging.info("Starting data collection")

    iris = load_iris(as_frame=True)
    df = iris.data.copy()
    df["species"] = iris.target.map(
        dict(enumerate(iris.target_names))
    )
    df["collected_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    output_path = Path("data/raw/iris_raw.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    logging.info("Data saved to %s", output_path)
    logging.info("Collected %d rows", len(df))

if __name__ == "__main__":
    collect_data()