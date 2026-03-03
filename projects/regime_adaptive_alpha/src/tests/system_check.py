# src/tests/system_check.py

import os
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from src.config.settings import settings, cfg, client


def run_system_check(
    test_symbol: str = "NVDA",
    start: str = "2025-12-01",
    end: str = "2025-12-03",
    timeframe: TimeFrame = TimeFrame.Minute,
    verbose: bool = True,
):
    """
    End-to-end check:
    - settings loads
    - env vars exist (without printing secrets)
    - Alpaca client works
    - small bars pull succeeds
    Returns the pulled dataframe.
    """

    if verbose:
        print("---- SETTINGS SUMMARY ----")
        print("Project root:", settings.project_root)
        print("Repo root:", settings.repo_root)
        print("Raw path:", settings.raw_path)
        print("Derived path:", settings.derived_path)
        print("Data feed:", settings.data_feed)

        print("\n---- ENV CHECK ----")
        print("ALPACA_API_KEY loaded:", os.getenv("ALPACA_API_KEY") is not None)
        print("ALPACA_SECRET_KEY loaded:", os.getenv("ALPACA_SECRET_KEY") is not None)

        print("\n---- API TEST PULL ----")

    request = StockBarsRequest(
        symbol_or_symbols=test_symbol,
        timeframe=timeframe,
        start=start,
        end=end,
        adjustment=cfg["data"]["adjustment"],
        feed=settings.data_feed,
    )

    bars = client.get_stock_bars(request).df

    if verbose:
        print("Rows pulled:", len(bars))
        print("Columns:", list(bars.columns))
        print("First timestamp:", bars.index.min())
        print("Last timestamp:", bars.index.max())

    return bars


if __name__ == "__main__":
    df = run_system_check()
    print("\nHead:")
    print(df.head())