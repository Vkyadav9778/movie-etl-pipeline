# transform.py
# Step 2 of the pipeline - cleans the raw data and splits it into
# smaller tables (this is basically the "T" in ETL).
#
# Why split into 4 tables instead of loading one big file?
# Because in the raw file every row repeats info like director/writer/star
# next to the movie name, budget, rating etc. Splitting it into
# movies / ratings / financials / people is closer to how you'd actually
# design tables in a warehouse, and it makes the SQL joins later
# actually mean something instead of just being one flat table.

import pandas as pd


def transform(df):
    df = df.copy()

    # drop rows where we don't even have a movie name, useless without it
    df = df.dropna(subset=["name"])

    # a few rows had duplicate names but were different movies (remakes etc)
    # so we can't use "name" as a real key, add our own id instead
    df = df.reset_index(drop=True)
    df.insert(0, "movie_id", df.index + 1)

    # basic cleanup
    df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
    df["gross"] = pd.to_numeric(df["gross"], errors="coerce")
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["votes"] = pd.to_numeric(df["votes"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    tables = {}

    tables["movies"] = df[
        ["movie_id", "name", "genre", "year", "runtime", "country", "company"]
    ]

    tables["ratings"] = df[["movie_id", "score", "votes", "rating"]]

    tables["financials"] = df[["movie_id", "budget", "gross"]]

    tables["people"] = df[["movie_id", "director", "writer", "star"]]

    total_rows = sum(len(t) for t in tables.values())
    print(f"Split into {len(tables)} tables, {total_rows} rows total")

    return tables


def save_tables(tables, out_dir="data/processed"):
    for name, table in tables.items():
        path = f"{out_dir}/{name}.csv"
        table.to_csv(path, index=False)
        print(f"Saved {path} ({len(table)} rows)")


if __name__ == "__main__":
    from extract import extract

    raw = extract()
    cleaned_tables = transform(raw)
    save_tables(cleaned_tables)
