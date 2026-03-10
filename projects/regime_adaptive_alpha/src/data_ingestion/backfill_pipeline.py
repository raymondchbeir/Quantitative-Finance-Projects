from datetime import datetime
import pandas as pd

from src.config.settings import DATA_DIR, START_YEAR, END_YEAR, client, TIMEZONE
from src.config.ticker_universe import TICKERS
from src.data_ingestion.fetch_bars import fetch_minute_bars
from src.data_ingestion.parquet_storage import save_to_parquet, parquet_exists


def get_safe_end():
    # conservative choice for historical storage:
    # stop at yesterday in New York time
    return (pd.Timestamp.now(tz=TIMEZONE) - pd.Timedelta(days=1)).normalize().tz_localize(None)


def run_backfill(symbols=None, start_year=None, end_year=None, overwrite=False):
    symbols = symbols or TICKERS
    start_year = start_year or START_YEAR
    end_year = end_year or END_YEAR

    safe_end = get_safe_end()
    current_year = safe_end.year

    for symbol in symbols:
        for year in range(start_year, end_year + 1):
            if not overwrite and parquet_exists(symbol, year, DATA_DIR):
                print(f"Skipping {symbol} {year} (already exists)")
                continue

            start = datetime(year, 1, 1)

            # normal historical years: go to Jan 1 of next year
            if year < current_year:
                end = datetime(year + 1, 1, 1)
            # current year: only pull data that can actually exist
            elif year == current_year:
                end = safe_end.to_pydatetime()
            # future years: skip
            else:
                print(f"Skipping {symbol} {year} (future year relative to safe end)")
                continue

            if end <= start:
                print(f"Skipping {symbol} {year} (no valid date range)")
                continue

            print(f"Fetching {symbol} {year} from {start} to {end}...")

            try:
                df = fetch_minute_bars(
                    client=client,
                    symbol=symbol,
                    start=start,
                    end=end,
                )

                if df.empty:
                    print(f"No data returned for {symbol} {year}")
                    continue

                file_path = save_to_parquet(df, symbol, year, DATA_DIR)
                print(f"Saved {symbol} {year} to {file_path}")

            except Exception as e:
                print(f"Failed for {symbol} {year}: {e}")


if __name__ == "__main__":
    run_backfill()