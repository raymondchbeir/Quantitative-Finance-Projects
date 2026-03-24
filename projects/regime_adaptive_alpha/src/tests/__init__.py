import pandas as pd

df = pd.read_parquet("AAPL_2016.parquet")

print(df.head())