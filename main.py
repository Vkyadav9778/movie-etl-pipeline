# main.py
# Runs the whole pipeline in order: extract -> transform -> load
# Run this from the project root: python main.py

from etl.extract import extract
from etl.transform import transform, save_tables
from etl.load import load_all

if __name__ == "__main__":
    print("STEP 1: Extract")
    raw_data = extract()

    print("\nSTEP 2: Transform")
    tables = transform(raw_data)
    save_tables(tables)

    print("\nSTEP 3: Load to Snowflake")
    load_all()

    print("\nPipeline finished.")
