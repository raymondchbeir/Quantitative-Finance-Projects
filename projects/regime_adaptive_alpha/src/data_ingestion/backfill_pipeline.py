from datetime import datetime

from src.config.ticker_universe import TICKERS
from src.config.settings import START_YEAR, END_YEAR, DATA_DIR
from src.data_ingestion.alpaca_client import get_alpaca_client
from src.data_ingestion.fetch_bars import fetch_minute_bars
from src.data_ingestion.parquet_storage import save_to_parquet


def run_backfill():
    client = get_alpaca_client()

    for symbol in TICKERS:
        for year in range(START_YEAR, END_YEAR + 1):
            start = datetime(year, 1, 1)
            end = datetime(year + 1, 1, 1)

            print(f"Fetching {symbol} {year}...")

            try:
                df = fetch_minute_bars(client, symbol, start, end)

                if df.empty:
                    print(f"No data returned for {symbol} {year}")
                    continue

                file_path = save_to_parquet(df, symbol, year, DATA_DIR)
                print(f"Saved {symbol} {year} to {file_path}")

            except Exception as e:
                print(f"Failed for {symbol} {year}: {e}")


if __name__ == "__main__":
    run_backfill()
