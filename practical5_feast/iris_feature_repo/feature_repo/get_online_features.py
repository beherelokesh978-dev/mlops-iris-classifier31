
from feast import FeatureStore

store = FeatureStore(repo_path=".")

features = [
    "iris_measurements:sepal length (cm)",
    "iris_measurements:sepal width (cm)",
    "iris_measurements:petal length (cm)",
    "iris_measurements:petal width (cm)",
    "iris_engineered_features:sepal_area",
    "iris_engineered_features:petal_area",
    "iris_engineered_features:sepal_to_petal_length_ratio",
    "iris_engineered_features:petal_length_bin",
]

result = store.get_online_features(
    features=features,
    entity_rows=[{"sample_id": 1}],
).to_dict()

print(result)