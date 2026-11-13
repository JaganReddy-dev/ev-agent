# Import the DuckDB library so Python can work with DuckDB databases
import duckdb

# Connect to a database file.
# If it doesn't exist, DuckDB creates it.
con = duckdb.connect("data/ev.duckdb")

# Read the CSV file and save its contents into a table called 'ev'
con.execute("""
    CREATE OR REPLACE TABLE ev AS
    SELECT *
    FROM read_csv_auto(
        'data/ev.csv',
        normalize_names = true
    )
""")

# Count how many rows are in the ev table and print the result
row = con.execute("SELECT COUNT(*) FROM ev").fetchone()
if row is None:
    raise RuntimeError("COUNT(*) query returned no result")
row_count = row[0]

print("Rows:", row_count)

# Print an empty line
print()

# Get information about every column in the ev table
columns = con.execute("DESCRIBE ev").fetchall()

# Go through each column and print its name and data type
for name, dtype, *_ in columns:
    print(f"{name:80} {dtype}")
