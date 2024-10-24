from pathlib import Path

import pandas as pd

fp = Path.cwd() / "data-raw"
fp_data = Path.cwd() / "data"

for file in fp.glob("*"):
    print(file)
    year = file.stem[-2:]
    newname = f"brfss20{year}"
    file_new = fp_data / f"{newname}.parquet"
    if file_new.exists():
        continue
    df = pd.read_sas(file)
    df.to_parquet(file_new)
    print(f"Saved {file_new}")
