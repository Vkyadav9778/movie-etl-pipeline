# Airbyte setup notes

This is how the ingestion part was actually set up using Airbyte (Airbyte Cloud, free tier). Writing it down here since it's not code, it's mostly UI config.

## Source

- Connector: **File / CSV**
- Pointed it at the raw `movies.csv` file
- Format: CSV, delimiter `;`, encoding ISO-8859-1 (had to check this with the `chardet` library first, the file wasn't in utf-8)

## Destination

- Connector: **Snowflake**
- Filled in:
  - Host / Account identifier
  - Warehouse
  - Database + Schema
  - Role
  - Username + password
- Loading method: Internal Staging (default option, no need for an S3 bucket for this size of data)

## Connection settings

- Sync mode: **Full refresh | Overwrite**
  (dataset is static, doesn't update, so no point doing incremental sync here. If this was a live dataset that gets new movies added every week, I'd switch this to Incremental)
- Schedule: Manual trigger (ran it manually after setting things up, didn't need it running every day for this project)
- Namespace: destination default

## What actually happens

1. Airbyte reads the raw CSV from the source
2. Pushes it into Snowflake as a raw landing table
3. From there, the cleaning/splitting into movies / ratings / financials / people tables is done with SQL + the transform.py script in this repo (the "T" part of ETL)

## Notes / things I ran into

- First sync failed because of the encoding issue mentioned above, had to explicitly set it in the source config
- Snowflake needed a dedicated warehouse + role for Airbyte to use, didn't want to use my main admin role for this
- Airbyte's own logs (under the connection -> Job history tab) were useful for checking row counts matched between source and destination
