 <<'EOF'
# Automated Data Pipeline

## Overview
This project implements an automated data pipeline using Python and DVC.

## Pipeline Stages

### 1. Data Collection
- Script: src/pipeline/collect.py
- Input: Iris dataset
- Output: data/raw/iris_raw.csv

### 2. Data Preprocessing
- Script: src/pipeline/preprocess.py
- Removes duplicate rows
- Converts measurements to numeric values
- Fills missing numeric values with the median
- Removes rows with missing species
- Output: data/processed/iris_preprocessed.csv

### 3. Feature Engineering
- Script: src/pipeline/features.py
- Creates sepal_area
- Creates petal_area
- Creates sepal_to_petal_length_ratio
- Creates petal_length_bin
- Output: data/processed/iris_features.csv

### 4. Data Validation
- Script: src/pipeline/validate.py
- Checks column names and order
- Checks missing values
- Checks allowed species
- Checks measurement ranges

## Pipeline Flow
Collect -> Preprocess -> Features -> Validate

## DVC Commands
Run the pipeline:
    dvc repro

View the pipeline:
    dvc dag

Upload DVC data:
    dvc push
EOF