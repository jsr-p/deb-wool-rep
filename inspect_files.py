from pathlib import Path

import pandas as pd

fp_data = Path.cwd() / "data"

for file in fp_data.glob("*"):
    df = pd.read_parquet(file)
    print(df.head())

    df.columns = df.columns.str.lower()

    print(is_in := "menthlth" in df.columns.str.lower())
    if is_in:
        print(df["menthlth"].describe())
        print(df["income2"])
    else:
        raise ValueError("No children column found")
    print(is_in := "children" in df.columns.str.lower())
    if is_in:
        print(df["children"].describe())
    else:
        raise ValueError("No children column found")

    print(is_in := "_chldcnt" in df.columns.str.lower())
    if is_in:
        print(df["_chldcnt"].describe())
    else:
        raise ValueError("No children column found")

    print(is_in := "educa" in df.columns.str.lower())
    if is_in:
        print(df["educa"].describe())
    else:
        raise ValueError("No children column found")
