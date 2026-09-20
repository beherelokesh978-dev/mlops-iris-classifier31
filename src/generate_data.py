import csv
import random
from pathlib import Path

random.seed(42)

output = Path("data/raw/iris_v1.csv")
output.parent.mkdir(parents=True, exist_ok=True)

rows = []

for i in range(150):
    if i < 50:
        sepal_length = random.uniform(4.3, 5.8)
        sepal_width = random.uniform(2.3, 4.4)
        petal_length = random.uniform(1.0, 1.9)
        petal_width = random.uniform(0.1, 0.6)
        species = "setosa"

    elif i < 100:
        sepal_length = random.uniform(4.9, 7.0)
        sepal_width = random.uniform(2.0, 3.4)
        petal_length = random.uniform(3.0, 5.0)
        petal_width = random.uniform(1.0, 1.8)
        species = "versicolor"

    else:
        sepal_length = random.uniform(4.9, 7.9)
        sepal_width = random.uniform(2.2, 3.8)
        petal_length = random.uniform(4.5, 6.9)
        petal_width = random.uniform(1.4, 2.5)
        species = "virginica"

    rows.append([
        round(sepal_length, 2),
        round(sepal_width, 2),
        round(petal_length, 2),
        round(petal_width, 2),
        species
    ])

with output.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species"
    ])
    writer.writerows(rows)

print(f"Dataset created: {output}")
print(f"Rows: {len(rows)}")