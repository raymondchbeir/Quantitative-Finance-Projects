from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def load_config(config_path: str = "configs/cleaning.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def find_parquet_files(raw_dir: Path) -> list[Path]:
    return sorted(raw_dir.rglob("*.parquet"))


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    rename_map = {}
    if "datetime" in df.columns and "timestamp" not in df.columns:
        rename_map["datetime"] = "timestamp"
    if "date" in df.columns and "timestamp" not in df.columns:
        rename_map["date"] = "timestamp"

    df = df.rename(columns=rename_map)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def normalize_timestamps(df: pd.DataFrame, market_tz: str) -> pd.DataFrame:
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert(market_tz)
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert(market_tz)

    df = df.sort_values("timestamp")
    return df


def drop_duplicate_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(subset=["timestamp"], keep="last").copy()


def filter_session_with_premarket(df: pd.DataFrame, market_open: str, market_close: str, premarket_bars: int, bar_minutes: int) -> pd.DataFrame:
    df = df.copy().set_index("timestamp")

    open_hour, open_minute = map(int, market_open.split(":"))
    total_premarket_minutes = premarket_bars * bar_minutes
    session_start_minutes = open_hour * 60 + open_minute - total_premarket_minutes

    start_hour = session_start_minutes // 60
    start_minute = session_start_minutes % 60
    session_start = f"{start_hour:02d}:{start_minute:02d}"

    df = df.between_time(session_start, market_close, inclusive="left")
    return df.reset_index()

def resample_to_5min(df: pd.DataFrame, output_bar_minutes: int) -> pd.DataFrame:
    df = df.copy().set_index("timestamp").sort_index()

    agg = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }

    if "symbol" in df.columns:
        symbol_value = df["symbol"].dropna().iloc[0] if not df["symbol"].dropna().empty else None
    else:
        symbol_value = None

    out = (
        df.resample(f"{output_bar_minutes}min", label="left", closed="left")
        .agg(agg)
        .dropna(subset=["open", "high", "low", "close"])
        .reset_index()
    )

    if symbol_value is not None:
        out["symbol"] = symbol_value

    return out


def expected_intraday_index(
    day_ts: pd.Timestamp,
    market_tz: str,
    market_open: str,
    market_close: str,
    premarket_bars: int,
    bar_minutes: int,
) -> pd.DatetimeIndex:
    day = pd.Timestamp(day_ts.date())

    open_hour, open_minute = map(int, market_open.split(":"))
    close_hour, close_minute = map(int, market_close.split(":"))

    total_premarket_minutes = premarket_bars * bar_minutes
    start_minutes = open_hour * 60 + open_minute - total_premarket_minutes

    start_hour = start_minutes // 60
    start_minute = start_minutes % 60

    start = pd.Timestamp(f"{day.date()} {start_hour:02d}:{start_minute:02d}", tz=market_tz)
    end = pd.Timestamp(f"{day.date()} {close_hour:02d}:{close_minute:02d}", tz=market_tz)

    return pd.date_range(
        start=start,
        end=end,
        freq=f"{bar_minutes}min",
        inclusive="left",
    )

def max_consecutive_true(values: list[bool]) -> int:
    max_run = 0
    current_run = 0
    for v in values:
        if v:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 0
    return max_run


def score_day(day_df: pd.DataFrame, symbol: str, trade_date: pd.Timestamp, config: dict) -> tuple[dict, pd.DataFrame]:
    market_tz = config["market_timezone"]
    rules = config["strict_rules"]
    bar_minutes = int(config["output_bar_minutes"])
    market_open = config["market_open"]
    market_close = config["market_close"]
    premarket_bars = int(config["premarket_bars"])

    expected_idx = expected_intraday_index(
        day_ts=trade_date,
        market_tz=market_tz,
        market_open=market_open,
        market_close=market_close,
        premarket_bars=premarket_bars,
        bar_minutes=bar_minutes,
    )
    expected_count = len(expected_idx)

    day_df = day_df.copy().set_index("timestamp").sort_index()
    reindexed = day_df.reindex(expected_idx)

    missing_mask = reindexed["open"].isna()
    missing_count = int(missing_mask.sum())

    open_window_bars = int(rules["open_window_bars"])
    close_window_bars = int(rules["close_window_bars"])

    regular_open_start = premarket_bars
    regular_open_end = premarket_bars + open_window_bars

    missing_open_window = bool(missing_mask.iloc[regular_open_start:regular_open_end].any())
    missing_close_window = bool(missing_mask.iloc[-close_window_bars:].any())
    max_consecutive_missing = max_consecutive_true(missing_mask.tolist())

    non_null_ohlcv = reindexed[["open", "high", "low", "close", "volume"]].notna().all().all()

    valid = True
    reason = "valid"

    if missing_count > int(rules["allow_missing_bars"]):
        valid = False
        reason = "too_many_missing_bars"
    elif rules["drop_if_missing_open_window"] and missing_open_window:
        valid = False
        reason = "missing_open_window"
    elif rules["drop_if_missing_close_window"] and missing_close_window:
        valid = False
        reason = "missing_close_window"
    elif max_consecutive_missing > int(rules["max_consecutive_missing"]):
        valid = False
        reason = "consecutive_missing_bars"
    elif rules["require_non_null_ohlcv"] and not non_null_ohlcv:
        valid = False
        reason = "null_ohlcv"

    report_row = {
        "symbol": symbol,
        "date": pd.Timestamp(trade_date.date()),
        "expected_bars": expected_count,
        "actual_bars": int(reindexed["open"].notna().sum()),
        "missing_bars": missing_count,
        "premarket_bars_expected": premarket_bars,
        "missing_open_window": missing_open_window,
        "missing_close_window": missing_close_window,
        "max_consecutive_missing": max_consecutive_missing,
        "valid_strict": valid,
        "drop_reason": reason,
    }

    cleaned_day = reindexed.reset_index().rename(columns={"index": "timestamp"})
    if valid:
        cleaned_day["symbol"] = symbol
        return report_row, cleaned_day

    return report_row, pd.DataFrame(columns=cleaned_day.columns)

def infer_symbol_from_path(path: Path) -> str:
    return path.stem.split("_")[0]


def clean_one_file(parquet_path: Path, config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    symbol = infer_symbol_from_path(parquet_path)

    df = pd.read_parquet(parquet_path)
    df = standardize_columns(df)
    df = normalize_timestamps(df, config["market_timezone"])
    df = drop_duplicate_timestamps(df)
    df = filter_session_with_premarket(
	df,
	 market_open=config["market_open"],
   	 market_close=config["market_close"],
   	 premarket_bars=int(config["premarket_bars"]),
   	 bar_minutes=int(config["output_bar_minutes"]),
)   	

    df = resample_to_5min(df, int(config["output_bar_minutes"]))

    df["trade_date"] = df["timestamp"].dt.date

    report_rows = []
    cleaned_days = []

    for trade_date, day_df in df.groupby("trade_date"):
        report_row, cleaned_day = score_day(
            day_df=day_df.drop(columns=["trade_date"]),
            symbol=symbol,
            trade_date=pd.Timestamp(trade_date),
            config=config,
        )
        report_rows.append(report_row)

        if not cleaned_day.empty:
            cleaned_days.append(cleaned_day)

    report_df = pd.DataFrame(report_rows)
    cleaned_df = pd.concat(cleaned_days, ignore_index=True) if cleaned_days else pd.DataFrame()

    return report_df, cleaned_df


def save_cleaned_output(cleaned_df: pd.DataFrame, src_path: Path, cleaned_root: Path) -> None:
    if cleaned_df.empty:
        return

    rel_parts = src_path.parts
    if "raw" in rel_parts:
        raw_idx = rel_parts.index("raw")
        relative_subpath = Path(*rel_parts[raw_idx + 1 :])
    else:
        relative_subpath = Path(src_path.name)

    out_path = cleaned_root / "strict" / relative_subpath
    out_path.parent.mkdir(parents=True, exist_ok=True)

    out_name = out_path.stem + "_cleaned.parquet"
    out_path = out_path.with_name(out_name)

    cleaned_df.to_parquet(out_path, index=False)


def main() -> None:
    config = load_config()

    raw_dir = Path(config["raw_data_dir"])
    cleaned_dir = Path(config["cleaned_data_dir"])
    reports_dir = Path(config["reports_dir"])

    reports_dir.mkdir(parents=True, exist_ok=True)
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    parquet_files = find_parquet_files(raw_dir)

    if not parquet_files:
        print(f"No parquet files found in {raw_dir}")
        return

    all_reports = []

    for i, parquet_path in enumerate(parquet_files, start=1):
        print(f"[{i}/{len(parquet_files)}] Processing {parquet_path}")
        try:
            report_df, cleaned_df = clean_one_file(parquet_path, config)
            all_reports.append(report_df)
            save_cleaned_output(cleaned_df, parquet_path, cleaned_dir)
        except Exception as e:
            print(f"Failed on {parquet_path}: {e}")

    if all_reports:
        final_report = pd.concat(all_reports, ignore_index=True)
        report_path = reports_dir / "day_quality_report.parquet"
        csv_path = reports_dir / "day_quality_report.csv"
        final_report.to_parquet(report_path, index=False)
        final_report.to_csv(csv_path, index=False)

        print("\nCleaning complete.")
        print(f"Saved report to: {report_path}")
        print(f"Saved report CSV to: {csv_path}")
        print(f"Valid strict days: {final_report['valid_strict'].mean():.2%}")
        print("\nDrop reasons:")
        print(final_report["drop_reason"].value_counts().head(10))
    else:
        print("No reports generated.")


if __name__ == "__main__":
    main()
