# extract.py
# Step 1 of the pipeline - just reads the raw movie data.
# The raw file was originally picked up through an Airbyte File source
# (CSV connector) and dropped here in data/raw/. This script simulates
# that same read so the pipeline can be run and tested locally.

import pandas as pd

RAW_FILE = "data/raw/movies.csv"


def extract():
    print("Reading raw file:", RAW_FILE)

    # the raw csv is semicolon separated and not in utf-8, found this out
    # using chardet while exploring the data the first time
    df = pd.read_csv(RAW_FILE, sep=";", quotechar='"', encoding="ISO-8859-1")

    print(f"Got {len(df)} rows and {len(df.columns)} columns")
    return df


if __name__ == "__main__":
    data = extract()
    print(data.head())
