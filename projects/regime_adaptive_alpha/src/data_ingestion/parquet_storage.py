from pathlib import Path
import pandas as pd


def get_parquet_path(symbol, year, base_dir):
    base_dir = Path(base_dir)
    return base_dir / symbol / f"{symbol}_{year}.parquet"


def parquet_exists(symbol, year, base_dir):
    path = get_parquet_path(symbol, year, base_dir)
    return path.exists()


def save_to_parquet(df, symbol, year, base_dir):
    base_dir = Path(base_dir)
    symbol_dir = base_dir / symbol
    symbol_dir.mkdir(parents=True, exist_ok=True)

    path = get_parquet_path(symbol, year, base_dir)

    df.to_parquet(
        path,
        engine="pyarrow",
        compression="snappy",
        index=False,
    )

    return path


def load_parquet(symbol, year, base_dir):
    path = get_parquet_path(symbol, year, base_dir)
    return pd.read_parquet(path)