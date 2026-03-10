import os
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient

load_dotenv()

def get_alpaca_client():

    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        raise ValueError("Missing Alpaca credentials")

    client = StockHistoricalDataClient(
        api_key=api_key,
        secret_key=secret_key
    )

    return client
