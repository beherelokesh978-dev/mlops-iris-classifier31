# Hyperparameter Tuning Analysis

## 1. Objective

The objective of this experiment is to compare a baseline Decision Tree model with Random Forest models tuned using Grid Search and Random Search.

The models were evaluated using 5-fold cross-validation with Macro F1 score.

## 2. Baseline Model

**Model:** Decision Tree Classifier

**Cross-Validation:** 5-fold

**Metric:** Macro F1 Score

**Test Accuracy:** 0.9333

**CV F1 Macro Mean:** 0.9328

The baseline model provides a reference point for comparing the performance of the tuned models.

## 3. Grid Search

**Model:** Random Forest Classifier

**Search Method:** Grid Search

**Total Parameter Combinations:** 72

**Cross-Validation:** 5-fold

**Total Fits:** 72 × 5 = 360

**Best CV F1 Macro:** 0.9583

**Test Accuracy:** 0.9667

Grid Search systematically evaluates every combination of the selected hyperparameters. It provides a thorough search but requires more computational time.

## 4. Random Search

**Model:** Random Forest Classifier

**Search Method:** Random Search

**Number of Iterations:** 30

**Cross-Validation:** 5-fold

**Total Fits:** 30 × 5 = 150

**Best CV F1 Macro:** 0.9581

**Test Accuracy:** 0.9667

Random Search evaluates a selected number of randomly chosen hyperparameter combinations. It requires fewer model fits than Grid Search while achieving similar performance in this experiment.

## 5. Comparison

| Model                       | CV F1 Macro | Test Accuracy | Total Fits |
| --------------------------- | ----------: | ------------: | ---------: |
| Baseline Decision Tree      |      0.9328 |        0.9333 |          5 |
| Grid Search Random Forest   |      0.9583 |        0.9667 |        360 |
| Random Search Random Forest |      0.9581 |        0.9667 |        150 |

## 6. Findings

1. Both tuned Random Forest models performed better than the baseline Decision Tree.
2. Grid Search achieved a CV F1 Macro score of 0.9583.
3. Random Search achieved a very similar CV F1 Macro score of 0.9581.
4. Both tuned models achieved a test accuracy of 0.9667.
5. Grid Search required 360 model fits.
6. Random Search required only 150 model fits.
7. Therefore, Random Search achieved comparable performance with less than half the number of model fits required by Grid Search.

## 7. Conclusion

Hyperparameter tuning improved the model performance compared with the baseline model.

Grid Search provides a systematic and exhaustive search of the selected parameter combinations. Random Search is more computationally efficient because it evaluates fewer combinations.

For this experiment, Random Search provided almost the same performance as Grid Search while requiring significantly fewer model fits.
