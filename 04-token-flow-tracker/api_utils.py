# api_utils.py

import requests
import pandas as pd
import streamlit as st

# Load Etherscan API key from secrets.toml
ETHERSCAN_API_KEY = st.secrets["ETHERSCAN_API_KEY"]

def fetch_token_transfers(contract_address, start_block=0, end_block=99999999, sort="asc"):
    """
    Fetch ERC-20 token transfer events for a given contract address.
    """
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": contract_address,
        "startblock": start_block,
        "endblock": end_block,
        "sort": sort,
        "apikey": ETHERSCAN_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] == "1":
            return pd.DataFrame(data["result"])
        else:
            st.warning(f"No data found: {data.get('message')}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Failed to fetch token transfers: {e}")
        return pd.DataFrame()
