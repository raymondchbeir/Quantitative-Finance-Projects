import pandas as pd

from src.config.settings import (
    PROJECT_NAME,
    PROJECT_ROOT,
    RAW_PATH,
    DERIVED_PATH,
    FEATURES_PATH,
    UNIVERSE_PATH,
    REPORTS_PATH,
    DATA_START,
    DATA_END,
    ADJUSTMENT,
    FEED,
    TIMEZONE,
    BASE_TIMEFRAME,
    DERIVED_TIMEFRAME,
    client,
)
from src.config.ticker_universe import TICKERS
from src.data_ingestion.fetch_bars import fetch_minute_bars


def run_system_check(
    test_symbol: str = "NVDA",
    start: str = "2024-01-03",
    end: str = "2024-01-05",
    verbose: bool = True,
):
    if verbose:
        print("---- SETTINGS SUMMARY ----")
        print("Project name:", PROJECT_NAME)
        print("Project root:", PROJECT_ROOT)
        print("Raw path:", RAW_PATH)
        print("Derived path:", DERIVED_PATH)
        print("Features path:", FEATURES_PATH)
        print("Universe path:", UNIVERSE_PATH)
        print("Reports path:", REPORTS_PATH)
        print("Configured data window:", DATA_START, "to", DATA_END)
        print("Adjustment:", ADJUSTMENT)
        print("Feed:", FEED)
        print("Timezone:", TIMEZONE)
        print("Base timeframe:", BASE_TIMEFRAME)
        print("Derived timeframe:", DERIVED_TIMEFRAME)
        print("Loaded tickers:", len(TICKERS))
        print("Testing symbol:", test_symbol)

    df = fetch_minute_bars(
        client=client,
        symbol=test_symbol,
        start=pd.Timestamp(start),
        end=pd.Timestamp(end),
    )

    if verbose:
        print("\n---- DATA CHECK ----")
        if df.empty:
            print("No data returned.")
        else:
            print(f"Pulled {len(df)} rows.")
            print("Columns:", list(df.columns))

    return df