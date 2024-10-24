"""
Script to construct (approximately the) data used in Deb & Wooldridge 2024.
https://www.nber.org/papers/w33026
"""

import polars as pl

rel_ages = [
    "18-24",
    "25-29",
    "30-34",
    "35-39",
    "40-44",
]

child_map = {
    ".": "Not asked or Missing",
    ".D": "DK/NS",
    ".R": "REFUSED",
    "1-87": "Number of children",
    "88": "None",
    "99": "Refused",
}

state_map = {
    # Download format from:
    # https://www.cdc.gov/brfss/annual_data/annual_2018.html
    1: "Alabama",
    2: "Alaska",
    4: "Arizona",
    5: "Arkansas",
    6: "California",
    8: "Colorado",
    9: "Connecticut",
    10: "Delaware",
    11: "District of Columbia",
    12: "Florida",
    13: "Georgia",
    15: "Hawaii",
    16: "Idaho",
    17: "Illinois",
    18: "Indiana",
    19: "Iowa",
    20: "Kansas",
    21: "Kentucky",
    22: "Louisiana",
    23: "Maine",
    24: "Maryland",
    25: "Massachusetts",
    26: "Michigan",
    27: "Minnesota",
    28: "Mississippi",
    29: "Missouri",
    30: "Montana",
    31: "Nebraska",
    32: "Nevada",
    33: "New Hampshire",
    34: "New Jersey",
    35: "New Mexico",
    36: "New York",
    37: "North Carolina",
    38: "North Dakota",
    39: "Ohio",
    40: "Oklahoma",
    41: "Oregon",
    42: "Pennsylvania",
    44: "Rhode Island",
    45: "South Carolina",
    46: "South Dakota",
    47: "Tennessee",
    48: "Texas",
    49: "Utah",
    50: "Vermont",
    51: "Virginia",
    53: "Washington",
    54: "WestVirginia",
    55: "Wisconsin",
    56: "Wyoming",
    66: "Guam",
    72: "Puerto Rico",
    78: "Virgin Islands",
    99: "Refused",
}

state_number_to_abbreviation = {
    1: "AL",  # Alabama
    2: "AK",  # Alaska
    4: "AZ",  # Arizona
    5: "AR",  # Arkansas
    6: "CA",  # California
    8: "CO",  # Colorado
    9: "CT",  # Connecticut
    10: "DE",  # Delaware
    11: "DC",  # District of Columbia
    12: "FL",  # Florida
    13: "GA",  # Georgia
    15: "HI",  # Hawaii
    16: "ID",  # Idaho
    17: "IL",  # Illinois
    18: "IN",  # Indiana
    19: "IA",  # Iowa
    20: "KS",  # Kansas
    21: "KY",  # Kentucky
    22: "LA",  # Louisiana
    23: "ME",  # Maine
    24: "MD",  # Maryland
    25: "MA",  # Massachusetts
    26: "MI",  # Michigan
    27: "MN",  # Minnesota
    28: "MS",  # Mississippi
    29: "MO",  # Missouri
    30: "MT",  # Montana
    31: "NE",  # Nebraska
    32: "NV",  # Nevada
    33: "NH",  # New Hampshire
    34: "NJ",  # New Jersey
    35: "NM",  # New Mexico
    36: "NY",  # New York
    37: "NC",  # North Carolina
    38: "ND",  # North Dakota
    39: "OH",  # Ohio
    40: "OK",  # Oklahoma
    41: "OR",  # Oregon
    42: "PA",  # Pennsylvania
    44: "RI",  # Rhode Island
    45: "SC",  # South Carolina
    46: "SD",  # South Dakota
    47: "TN",  # Tennessee
    48: "TX",  # Texas
    49: "UT",  # Utah
    50: "VT",  # Vermont
    51: "VA",  # Virginia
    53: "WA",  # Washington
    54: "WV",  # West Virginia
    55: "WI",  # Wisconsin
    56: "WY",  # Wyoming
    66: "GU",  # Guam
    72: "PR",  # Puerto Rico
    78: "VI",  # Virgin Islands
    99: "Refused",  # Refused
}

year_to_state_abbreviation = {
    2007: ["ID"],  # Idaho
    2008: ["SC"],  # South Carolina
    2009: ["AZ"],  # Arizona
    2012: ["UT"],  # Utah
    2013: ["AL"],  # Alabama
    2014: ["GA", "MO", "RI", "TN"],  # Georgia, Missouri, Rhode Island, Tennessee
    2015: ["NM"],  # New Mexico
    2017: ["CT", "OH"],  # Connecticut, Ohio
    2018: ["KY"],  # Kentucky
    "Never treated": [
        "AK",
        "CA",
        "DE",
        "HI",
        "IA",
        "KS",
        "ME",
        "MI",
        "MS",
        "MT",
        "NE",
        "NH",
        "NJ",
        "NY",
        "NC",
        "OR",
        "PA",
        "VT",
        "WA",
        "WV",
        "WY",
    ],  # States never treated with punitive policies
}
treat_map = {
    state: year if isinstance(year, int) else 0
    for year, states in year_to_state_abbreviation.items()
    for state in states
}


all_data = (
    pl.read_parquet("brfss2005-2018.parquet")
    .filter(
        pl.col("sex").eq("female"),
        pl.col("age").is_in(rel_ages),
    )
    .drop("file")
    .with_columns(
        state_name=pl.col("state")
        .cast(pl.Int32)
        .replace_strict(state_map)
        .cast(pl.String),
        state_abv=pl.col("state")
        .cast(pl.Int32)
        .replace_strict(state_number_to_abbreviation)
        .cast(pl.String),
    )
)

print("Processed data:")
print(all_data)
print(all_data.glimpse())


states = [state for v in year_to_state_abbreviation.values() for state in v]

all_data.select("child1", "child2").describe()
all_data.select(
    pl.col("child2").filter(pl.col("child2").is_in(range(1, 7))).sum(),
    pl.col("child1").filter(pl.col("child1").is_in(range(1, 88))).sum(),
)


all_data.filter(pl.col("state_abv").eq("ID")).select("mental_health").mean()
all_data.filter(pl.col("state_abv").eq("ID")).select("mental_health").mean()

all_data = (
    all_data.filter(
        pl.col("child1").is_in(range(1, 88)),
        # pl.col("child2").is_in(range(2, 6 + 1)),
        pl.col("state_abv").is_in(states),
        # pl.col("mental_health").is_in(range(1, 30 + 1)),
        # pl.col("pm_health").is_in(range(1, 30 + 1)),
    )
    .with_columns(
        treat_year=pl.col("state_abv").replace_strict(treat_map).cast(pl.Int32),
        good_mh=pl.lit(30).sub(pl.col("mental_health")),
    )
    .with_columns(
        treated=pl.col("year").cast(pl.Int32).gt(pl.col("treat_year")),
    )
)


all_data["mental_health"].value_counts()
all_data["mental_health"].describe()

print(all_data)
print("Counts by year:")
print(all_data.group_by("treat_year").agg(pl.len().alias("n")).sort("treat_year"))
print(
    all_data.group_by("treated").agg(
        pl.col("mental_health").mean(),
        pl.col("good_mh").mean(),
        pl.col("pm_health").mean(),
        pl.col("child1").mean(),
        pl.col("child2").mean(),
    )
)
print(f"Total number of observations: {len(all_data)}")


all_data.write_parquet("debwool.parquet")
print("Wrote processed data to debwool.parquet")
