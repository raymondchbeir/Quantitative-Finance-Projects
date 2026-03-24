import numpy as np
import pandas as pd


def bars_since(condition: pd.Series) -> pd.Series:
    result = np.full(len(condition), np.nan)
    last_true_idx = -1

    for i, flag in enumerate(condition):
        if flag:
            last_true_idx = i
            result[i] = 0
        elif last_true_idx >= 0:
            result[i] = i - last_true_idx

    return pd.Series(result, index=condition.index)


def add_cross_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["bull_cross"] = (
        (df["ema_9"] > df["ema_20"]) &
        (df["ema_9"].shift(1) <= df["ema_20"].shift(1))
    )

    df["bear_cross"] = (
        (df["ema_9"] < df["ema_20"]) &
        (df["ema_9"].shift(1) >= df["ema_20"].shift(1))
    )

    df["bars_since_bull_cross"] = bars_since(df["bull_cross"])
    df["bars_since_bear_cross"] = bars_since(df["bear_cross"])

    return df


def add_structural_features(
    df: pd.DataFrame,
    cross_freshness: int = 3,
    atr_threshold: float | None = None,
    session_start: str = "09:30",
    session_end: str = "15:55"
) -> pd.DataFrame:
    df = df.copy()

    df["bull_fresh"] = df["bars_since_bull_cross"] <= cross_freshness
    df["bear_fresh"] = df["bars_since_bear_cross"] <= cross_freshness

    df["above_vwap"] = df["close"] > df["vwap"]
    df["below_vwap"] = df["close"] < df["vwap"]

    df["above_hma"] = df["close"] > df["hma_20"]
    df["below_hma"] = df["close"] < df["hma_20"]

    df["hma_up"] = df["hma_20"] > df["hma_20"].shift(1)
    df["hma_down"] = df["hma_20"] < df["hma_20"].shift(1)

    df["vwap_slope_up"] = df["vwap_slope_5"] > 0
    df["vwap_slope_down"] = df["vwap_slope_5"] < 0

    if atr_threshold is None:
        df["vol_ok"] = True
    else:
        df["vol_ok"] = df["atr_14"] >= atr_threshold

    intraday_time = df.index.strftime("%H:%M")
    df["session_ok"] = (intraday_time >= session_start) & (intraday_time <= session_end)

    return df


def add_entry_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["long_entry"] = (
        df["bull_fresh"] &
        df["above_vwap"] &
        df["above_hma"] &
        df["hma_up"] &
        df["vwap_slope_up"] &
        df["vol_ok"] &
        df["session_ok"]
    )

    df["short_entry"] = (
        df["bear_fresh"] &
        df["below_vwap"] &
        df["below_hma"] &
        df["hma_down"] &
        df["vwap_slope_down"] &
        df["vol_ok"] &
        df["session_ok"]
    )

    return df


def add_model_a_signal_features(
    df: pd.DataFrame,
    cross_freshness: int = 3,
    atr_threshold: float | None = None,
    session_start: str = "09:30",
    session_end: str = "15:55"
) -> pd.DataFrame:
    df = add_cross_features(df)
    df = add_structural_features(
        df,
        cross_freshness=cross_freshness,
        atr_threshold=atr_threshold,
        session_start=session_start,
        session_end=session_end
    )
    df = add_entry_signals(df)

    return df
