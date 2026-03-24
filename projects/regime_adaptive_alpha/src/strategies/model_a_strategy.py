def generate_signals(df):
    df["long_entry"] = (
        (df["ema_9"] > df["ema_20"]) &
        (df["close"] > df["vwap"])
    )

    df["short_entry"] = (
        (df["ema_9"] < df["ema_20"]) &
        (df["close"] < df["vwap"])
    )

    return df
