import pandas as pd
from src.indicators.model_a_indicators import add_model_a_indicators
from src.signals.model_a_signals import add_model_a_signal_features

print("Loading data...")

df = pd.read_parquet("data/cleaned/strict/NVDA")
print(df.columns)
print(type(df.index))
print(df.head())

print("Index type after indicators:")
print(type(df.index))

print("Adding signal features...")
df = add_model_a_signal_features(df, cross_freshness=3)

print("\nSignal counts:")
print("Bull crosses:", int(df["bull_cross"].sum()))
print("Bear crosses:", int(df["bear_cross"].sum()))
print("Long entries:", int(df["long_entry"].sum()))
print("Short entries:", int(df["short_entry"].sum()))

print("\nRecent signal rows:")
print(df[[
    "close",
    "ema_9",
    "ema_20",
    "vwap",
    "hma_20",
    "bull_cross",
    "bear_cross",
    "long_entry",
    "short_entry"
]].tail(20))
