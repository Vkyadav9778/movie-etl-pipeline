# load.py
# Step 3 of the pipeline - loads the cleaned csv files into Snowflake.
#
# In the actual project the loading part was handled by Airbyte
# (File source -> Snowflake destination connector, scheduled sync).
# This script does the same thing in plain Python/SQL so the whole
# pipeline can also be run and tested without Airbyte set up.

import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TABLES = ["movies", "ratings", "financials", "people"]


def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )


def create_tables(conn):
    with open("sql/01_create_tables.sql") as f:
        create_sql = f.read()

    cur = conn.cursor()
    # the sql file has multiple statements separated by ;
    for statement in create_sql.split(";"):
        statement = statement.strip()
        if statement:
            cur.execute(statement)
    cur.close()
    print("Tables ready")


def load_table(conn, table_name):
    path = f"data/processed/{table_name}.csv"
    df = pd.read_csv(path)

    # snowflake likes uppercase column names by default
    df.columns = [c.upper() for c in df.columns]

    success, chunks, rows, _ = write_pandas(conn, df, table_name.upper())
    print(f"Loaded {table_name}: {rows} rows, success={success}")


def load_all():
    conn = get_connection()
    create_tables(conn)
    for table in TABLES:
        load_table(conn, table)
    conn.close()
    print("Done loading everything into Snowflake")


if __name__ == "__main__":
    load_all()
