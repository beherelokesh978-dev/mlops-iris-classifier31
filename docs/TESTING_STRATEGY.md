
# Testing Strategy

## Objective
To test the data preprocessing, feature engineering, data validation,
model training, and model quality stages of the Iris ML pipeline.

## Test Files

1. test_preprocess.py - Tests data cleaning and missing values.
2. test_features.py - Tests feature calculations and petal categories.
3. test_validate.py - Tests data validation rules.
4. test_training_pipeline.py - Tests model training and predictions.
5. test_model_quality.py - Tests model predictions and accuracy.

## Test Execution
Run all tests using:

pytest --cov=src --cov-report=term-missing --junitxml=test-results.xml

## Expected Result
All tests should pass when the code, dependencies, and required dataset are correct.

## Conclusion
Unit testing helps detect errors early and improves the reliability
of the machine learning pipeline.
