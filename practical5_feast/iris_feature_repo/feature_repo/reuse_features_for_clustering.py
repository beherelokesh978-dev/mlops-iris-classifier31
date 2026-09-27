
from feast import FeatureStore

store = FeatureStore(repo_path=".")

feature_service = store.get_feature_service(
    "iris_feature_service"
)

result = store.get_online_features(
    features=feature_service,
    entity_rows=[{"sample_id": 1}],
).to_dict()

print("Reused features:")
print(result)