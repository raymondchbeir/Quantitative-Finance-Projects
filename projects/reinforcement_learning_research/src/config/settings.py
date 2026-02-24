from pathlib import Path

# Repo root = two levels up from this file (src/config/settings.py)
REPO_ROOT = Path(__file__).resolve().parents[2]

BASE_FOLDER_RAW = REPO_ROOT / "data" / "raw"
BASE_FOLDER_PROCESSED = REPO_ROOT / "data" / "processed"

SYMBOLS = ["NVDA", "PLTR"]
START = "2016-01-01"
END = "2026-01-30"
