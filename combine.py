import re
from pathlib import Path

import pandas as pd

fp = Path.cwd() / "clean"

all_data = pd.concat(
    [pd.read_csv(file).assign(file=file.stem) for file in fp.glob("*.csv")]
).reset_index(drop=True)
all_data.drop(columns=["Unnamed: 0"], inplace=True)

print(all_data.head())
print(all_data.describe())


cat_cols = [
    "income",
    "race",
    "state",
    "age",
    "sex",
    "child1",
    "child2",
]
num_cols = [
    "height",
    "weight",
    "bmi",
    "mental_health",
]

re_year = re.compile(r"\d{4}")
all_data = all_data.assign(
    year=all_data["file"].apply(lambda x: int(re_year.search(x).group()))
)

print("By year:")
for col in cat_cols:
    print(all_data.groupby("year")[col].value_counts())

for col in num_cols:
    print(all_data.groupby("year")[col].describe())


print("Overall:")
for col in cat_cols:
    print(f"----------{col}----------")
    print(all_data[col].value_counts())

for col in num_cols:
    print(f"----------{col}----------")
    print(all_data[col].describe())


all_data.to_parquet("brfss2005-2018.parquet")
