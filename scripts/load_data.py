# Import the DuckDB Connection and DIR's to work with

from ev_agent.db import get_connection, CSV_PATH

# Connect to a database file.
# If it doesn't exist, DuckDB creates it.
with get_connection() as con:
    con.execute(f"""
    CREATE OR REPLACE TABLE ev_raw AS
    SELECT * FROM read_csv_auto('{CSV_PATH}', normalize_names = true)
    """)
    row = con.execute("SELECT COUNT(*) FROM ev_raw").fetchone()
    if row is None:
        raise RuntimeError("COUNT(*) query returned no result")
    print(f"Loaded ev_raw: {row[0]} rows")