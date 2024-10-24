import polars as pl

all_data = pl.read_parquet("debwool.parquet").with_columns(
    black=pl.col("race").eq("black"),
    hispanic=pl.col("race").eq("hispanic"),
)


all_data["income"].value_counts()

print("Processed data:")
print(all_data)

print("Counts by year:")
print(all_data.group_by("treat_year").agg(pl.len().alias("n")).sort("treat_year"))

with pl.Config(tbl_rows=100):
    print(
        all_data["mental_health"].value_counts().sort("mental_health"),
        all_data["pm_health"].value_counts().sort("pm_health"),
        sep="\n",
    )

"""
1  Never attended school or only kindergarten  680  0.14  0.30  
2  Grades 1 through 8 (Elementary)  13,450  2.74  4.85  
3  Grades 9 through 11 (Some high school)  28,219  5.74  10.06  
4  Grade 12 or GED (High school graduate)  143,592  29.20  28.53  
5  College 1 year to 3 years (Some college or technical school)  134,835  27.42  30.77  
6  College 4 years or more (College graduate)  170,997  34.77  25.49
"""
print("Mental health")
print(
    all_data.group_by("treated").agg(
        pl.col("mental_health").mean(),
        pl.col("pm_health").mean(),
        pl.col("edu").eq(4).mean().alias("HS or GED").round(3),
        pl.col("edu").eq(5).mean().alias("Some college").round(3),
        pl.col("edu").eq(6).mean().alias("Bachelors or more").round(3),
        pl.len().alias("#obs"),
    )
)
