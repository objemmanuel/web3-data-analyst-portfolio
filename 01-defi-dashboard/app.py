# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from api_utils import get_uniswap_tvl, get_uniswap_tvl_history, get_token_price


st.set_page_config(page_title="DeFi Protocol Dashboard", layout="wide")
st.title("📊 Real-Time DeFi Protocol Dashboard")
st.markdown("Track TVL (Total Value Locked) for Uniswap in real-time using [DefiLlama](https://defillama.com/) API.")

# Current TVL Metric
st.subheader("🔹 Uniswap TVL (Current)")

data = get_uniswap_tvl()

if isinstance(data, dict) and "tvl" in data:
    st.metric(label="Uniswap TVL (USD)", value=f"${data['tvl']:,.2f}")
else:
    error_message = data["error"] if isinstance(data, dict) and "error" in data else str(data)
    st.error(f"Failed to fetch data: {error_message}")

# Historical TVL Chart
st.subheader("📈 Historical TVL (Uniswap)")

tvl_history = get_uniswap_tvl_history()

if tvl_history:
    df = pd.DataFrame(tvl_history)
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df = df[df['totalLiquidityUSD'] > 0]  # Remove bad zero entries

    fig = px.line(df, x="date", y="totalLiquidityUSD",
                  title="Uniswap TVL Over Time",
                  labels={"totalLiquidityUSD": "TVL (USD)", "date": "Date"},
                  template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No historical TVL data available.")

# Token Price Tracker
st.subheader("💰 UNI Token Price (via CoinGecko)")

token_data = get_token_price("uniswap")

if isinstance(token_data, dict) and "price" in token_data and token_data["price"]:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Price (USD)", f"${token_data['price']:,.2f}")
    col2.metric("Market Cap", f"${token_data['market_cap']:,.0f}")
    col3.metric("24h Change", f"{token_data['change_24h']:.2f}%")
    col4.metric("Volume (24h)", f"${token_data['volume']:,.0f}")
else:
    st.warning(f"Could not fetch token data: {token_data.get('error', 'Unknown')}")
