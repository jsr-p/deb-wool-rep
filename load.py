import pandas as pd

df = pd.read_sas("CDBRFS05.XPT")
print(df)
df.to_parquet("CDBRFS05.parquet")
