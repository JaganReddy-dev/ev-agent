from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).parents[2]
DATA_DIR = PROJECT_ROOT/"data"
CSV_PATH = DATA_DIR/"ev.csv"
DB_PATH = DATA_DIR/"ev.duckdb"

def get_connection(read_only:bool = False) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH), read_only=read_only)