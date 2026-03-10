from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import pandas as pd


def fetch_minute_bars(client, symbol, start, end):
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=start,
        end=end
    )

    bars = client.get_stock_bars(request)
    df = bars.df.copy()

    if df.empty:
        return pd.DataFrame()

    return df
