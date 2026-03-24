import numpy as np
import pandas as pd


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def wma(series: pd.Series, period: int) -> pd.Series:
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(
        lambda x: np.dot(x, weights) / weights.sum(),
        raw=True
    )


def hma(series: pd.Series, period: int) -> pd.Series:
    half_period = int(period / 2)
    sqrt_period = int(np.sqrt(period))

    wma_half = wma(series, half_period)
    wma_full = wma(series, period)
    raw_hma = 2 * wma_half - wma_full

    return wma(raw_hma, sqrt_period)


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    ema_fast = ema(series, fast)
    ema_slow = ema(series, slow)

    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line

    return macd_line, signal_line, hist


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    prev_close = df["close"].shift(1)

    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - prev_close).abs()
    tr3 = (df["low"] - prev_close).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def intraday_vwap(df: pd.DataFrame) -> pd.Series:
    df = df.copy()

    if not isinstance(df.index, pd.DatetimeIndex):
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.set_index("timestamp")
        elif "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.set_index("datetime")
        else:
            raise ValueError(
                "DataFrame must have a DatetimeIndex or a 'timestamp'/'datetime' column."
            )

    df = df.sort_index()

    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    tpv = typical_price * df["volume"]

    session_key = pd.Series(df.index.date, index=df.index)
    cumulative_tpv = tpv.groupby(session_key).cumsum()
    cumulative_volume = df["volume"].groupby(session_key).cumsum()

    return cumulative_tpv / cumulative_volume


def add_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["date"] = df.index.date
    df["time"] = df.index.time
    df["hour"] = df.index.hour
    df["minute"] = df.index.minute
    df["tod_bucket"] = df.index.strftime("%H:%M")

    return df


def add_model_a_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.set_index("timestamp")
    elif "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.set_index("datetime")

    df = df.sort_index()

    df["ema_9"] = ema(df["close"], 9)
    df["ema_20"] = ema(df["close"], 20)
    df["hma_20"] = hma(df["close"], 20)
    df["rsi_14"] = rsi(df["close"], 14)

    macd_line, signal_line, hist = macd(df["close"])
    df["macd"] = macd_line
    df["macd_signal"] = signal_line
    df["macd_hist"] = hist

    df["atr_14"] = atr(df, 14)
    df["vwap"] = intraday_vwap(df)
    df["vwap_slope_5"] = df["vwap"].diff(5)

    df = add_time_columns(df)

    return df
