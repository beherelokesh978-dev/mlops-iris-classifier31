import pandas as pd
from pathlib import Path

# Input CSV from Experiment 4
input_file = Path(
    "../../../data/processed/iris_features.csv"
).resolve()

# Output Parquet file for Feast
output_file = Path("data/iris_features.parquet")

# Read CSV
df = pd.read_csv(input_file)

# Create entity ID
df.insert(0, "sample_id", range(len(df)))

# Create timestamps
start_time = pd.Timestamp(
    "2026-08-15 15:20:02",
    tz="UTC"
)

df["event_timestamp"] = pd.date_range(
    start=start_time,
    periods=len(df),
    freq="min"
)

df["created_timestamp"] = df["event_timestamp"]

# Create output folder
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save Parquet file
df.to_parquet(output_file, index=False)

print(f"Wrote {len(df)} rows to {output_file}")