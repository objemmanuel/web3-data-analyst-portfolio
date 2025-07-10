# model_utils.py

import requests
import pandas as pd
from prophet import Prophet
from datetime import datetime

def fetch_historical_data(token_id="ethereum", days=90, vs_currency="usd"):
    """
    Fetch historical market data for a token from CoinGecko.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days,
        "interval": "daily"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["ds", "y"])
    df["ds"] = pd.to_datetime(df["ds"], unit='ms')
    return df

def train_forecast_model(df):
    """
    Train Prophet model and return forecast DataFrame.
    """
    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=15)
    forecast = model.predict(future)
    return forecast, model
