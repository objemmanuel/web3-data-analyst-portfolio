# app.py

import streamlit as st
import plotly.graph_objects as go
from model_utils import fetch_historical_data, train_forecast_model

st.set_page_config(page_title="Token Price Predictor", layout="wide")
st.title("📈 Token Price / TVL Forecasting App")

# Select token and forecast days
token = st.selectbox("Choose a token", ["ethereum", "uniswap", "aave", "usd-coin"])
forecast_days = st.slider("Forecast how many days?", 7, 30, 15)

# Fetch data
st.info("Fetching historical price data...")
df = fetch_historical_data(token_id=token, days=90)

if not df.empty:
    st.success("✅ Data loaded!")

    # Show raw data
    with st.expander("📄 View Raw Data"):
        st.dataframe(df)

    # Train model and forecast
    forecast, model = train_forecast_model(df)

    # Merge forecast with actual
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["ds"], y=df["y"], mode='lines', name='Historical Price'))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], mode='lines', name='Forecast'))

    st.plotly_chart(fig, use_container_width=True)

    # Show forecast table
    st.subheader("🔮 Forecast Table")
    st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(forecast_days))

else:
    st.error("Failed to fetch data from CoinGecko.")
