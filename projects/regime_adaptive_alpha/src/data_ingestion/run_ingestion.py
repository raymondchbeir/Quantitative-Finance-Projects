from tqdm.auto import tqdm

from src.config.settings import START_YEAR, END_YEAR
from src.config.ticker_universe import TICKERS
from src.data_ingestion.backfill_pipeline import run_backfill


def run_full_backfill(start_year=None, end_year=None, overwrite=False):
    start_year = start_year or START_YEAR
    end_year = end_year or END_YEAR

    num_years = end_year - start_year + 1
    total_jobs = len(TICKERS) * num_years

    print("You are about to run a full-universe backfill.")
    print(f"Number of tickers: {len(TICKERS)}")
    print(f"Years: {start_year} to {end_year}")
    print(f"Total symbol-year jobs: {total_jobs}")
    print(f"Overwrite existing files: {overwrite}")

    response = input("Type 'yes' to continue: ").strip().lower()

    if response != "yes":
        print("Full backfill cancelled.")
        return

    for symbol in tqdm(TICKERS, desc="Backfilling symbols", unit="symbol"):
        run_backfill(
            symbols=[symbol],
            start_year=start_year,
            end_year=end_year,
            overwrite=overwrite,
        )

    print("Full backfill complete.")


if __name__ == "__main__":
    run_full_backfill()