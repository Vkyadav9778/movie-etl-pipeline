# Movie Dataset ETL Pipeline

An end-to-end ETL pipeline for a movie dataset (~4,000 movies, 16,000+ rows once split across tables). Data is ingested with Airbyte and loaded into Snowflake, then queried with SQL for some basic insights.

I built this to actually learn how a real ETL pipeline is put together - not just clean a CSV in pandas and call it done, but take it through ingestion, transformation and loading into an actual cloud warehouse, and then write SQL on top of it.

## Tech used

- **Python / pandas** - reading and cleaning the data
- **Airbyte** - moving data from the raw CSV source into Snowflake
- **Snowflake** - the data warehouse where the final tables live
- **SQL** - joins, filters and aggregations on the loaded tables

## Dataset

Raw data is a single CSV with movie name, genre, year, rating, score, votes, director, writer, star, country, budget, gross, company, runtime for ~4,000 movies.

During the transform step this gets split into 4 tables connected by a `movie_id`:

- `movies` - name, genre, year, runtime, country, company
- `ratings` - score, votes, MPAA rating
- `financials` - budget, gross
- `people` - director, writer, star

## How it works

```
raw movies.csv
      |
      v
   Airbyte  --->  Snowflake (raw landing table)
      |
      v
 transform.py (python/pandas)
      |
      v
 movies / ratings / financials / people  --->  loaded into Snowflake
      |
      v
        SQL queries (joins, group by, filters)
```

Steps in order:

1. **Extract** - `etl/extract.py` reads the raw csv (semicolon separated, ISO-8859-1 encoded)
2. **Transform** - `etl/transform.py` cleans the data, adds a `movie_id`, and splits it into the 4 tables above
3. **Load** - `etl/load.py` creates the tables in Snowflake and loads the csv files into them
4. **Analyze** - the `sql/` folder has the actual SQL used to pull insights out (highest grossing movies, avg rating per genre, most active directors etc.)

Airbyte was used for the source -> destination sync into Snowflake, notes on how that was configured are in [`airbyte/airbyte_setup.md`](airbyte/airbyte_setup.md).

## Running it

```bash
pip install -r requirements.txt

# just extract + transform, no snowflake needed
python etl/transform.py

# full pipeline including snowflake load (needs a .env file, see .env.example)
python main.py
```

## Folder structure

```
movie-etl-pipeline/
├── data/
│   ├── raw/            raw csv (source data)
│   └── processed/      cleaned + split tables
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_joins.sql
│   ├── 03_aggregations.sql
│   └── 04_filters.sql
├── airbyte/
│   └── airbyte_setup.md
├── main.py
└── requirements.txt
```

## What I'd add next

- Incremental sync in Airbyte instead of full refresh, if the dataset ever gets updated
- Some kind of scheduling (dbt / Airflow) instead of running main.py by hand
- Data quality checks before loading (right now transform.py just drops rows with no name)
