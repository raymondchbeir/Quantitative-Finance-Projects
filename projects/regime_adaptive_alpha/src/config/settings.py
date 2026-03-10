from pathlib import Path
import yaml
from dotenv import load_dotenv

from src.data_ingestion.alpaca_client import get_alpaca_client

# Project root: regime_adaptive_alpha/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "configs"

load_dotenv()


def load_yaml(filename: str):
    path = CONFIG_DIR / filename
    with open(path, "r") as f:
        return yaml.safe_load(f)


# Full config dict
settings = load_yaml("default.yaml")
cfg = settings

# Project
PROJECT_NAME = settings["project"]["name"]

# Data config
DATA_START = settings["data"]["start"]
DATA_END = settings["data"]["end"]
ADJUSTMENT = settings["data"]["adjustment"]
FEED = settings["data"]["feed"]
TIMEZONE = settings["data"]["timezone"]
INCLUDE_PREMARKET = settings["data"]["include_premarket"]

# Aggregation
BASE_TIMEFRAME = settings["aggregation"]["base_timeframe"]
DERIVED_TIMEFRAME = settings["aggregation"]["derived_timeframe"]

# Storage
RAW_PATH = PROJECT_ROOT / settings["storage"]["raw_path"]
DERIVED_PATH = PROJECT_ROOT / settings["storage"]["derived_path"]
FEATURES_PATH = PROJECT_ROOT / settings["storage"]["features_path"]
UNIVERSE_PATH = PROJECT_ROOT / settings["storage"]["universe_path"]
REPORTS_PATH = PROJECT_ROOT / settings["storage"]["reports_path"]

# Backward-compatible aliases for older code
DATA_DIR = RAW_PATH
START_YEAR = int(DATA_START[:4])
END_YEAR = int(DATA_END[:4])

# Shared Alpaca client
client = get_alpaca_client()