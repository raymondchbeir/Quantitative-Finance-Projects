import pandas as pd
from src.indicators.model_a_indicators import add_model_a_indicators

print("Loading data...")

df = pd.read_parquet("data/cleaned/strict/NVDA")

# use the real timestamp column
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")
df = df.sort_index()

print("Adding indicators...")

df = add_model_a_indicators(df)

print("\nColumns:")
print(df.columns)

print("\nIndex type:")
print(type(df.index))

print("\nFirst timestamp:")
print(df.index[0])

print("\nLast rows:")
print(df[[
    "close",
    "ema_9",
    "ema_20",
    "hma_20",
    "rsi_14",
    "macd",
    "vwap",
    "atr_14"
]].tail())
