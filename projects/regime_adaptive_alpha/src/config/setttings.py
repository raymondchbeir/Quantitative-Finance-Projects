from pathlib import Path

# Root of the project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Where parquet files will be stored
DATA_DIR = PROJECT_ROOT / "data" / "minute_bars"

# Backfill range
START_YEAR = 2024
END_YEAR = 2024
