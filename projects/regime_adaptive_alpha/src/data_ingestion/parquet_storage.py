import os
import pandas as pd


def save_to_parquet(df, symbol, year, base_dir="data/minute_bars"):

    os.makedirs(f"{base_dir}/{symbol}", exist_ok=True)

    path = f"{base_dir}/{symbol}/{symbol}_{year}.parquet"

    df.to_parquet(
        path,
        engine="pyarrow",
        compression="snappy",
        index=True
    )

    return path
