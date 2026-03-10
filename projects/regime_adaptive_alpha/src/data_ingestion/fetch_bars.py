import pandas as pd
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from src.config.settings import ADJUSTMENT, FEED


def get_effective_end(end=None):
    if end is not None:
        return pd.Timestamp(end)

    return (pd.Timestamp.now(tz="America/New_York") - pd.Timedelta(days=1)).normalize()


def fetch_minute_bars(client, symbol, start, end=None):
    effective_end = get_effective_end(end)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=pd.Timestamp(start),
        end=effective_end,
        adjustment=ADJUSTMENT,
        feed=FEED,
    )

    bars = client.get_stock_bars(request)
    df = bars.df.copy()

    if df.empty:
        return pd.DataFrame()

    return df.reset_index()