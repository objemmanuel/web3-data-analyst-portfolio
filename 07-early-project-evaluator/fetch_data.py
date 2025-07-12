import requests
import streamlit as st

# Load API Key securely
COVALENT_API_KEY = st.secrets["COVALENT_API_KEY"]

# ----------------------------
# 1. Fetch TVL via Covalent (ERC20 token balances of a contract or address)
# ----------------------------
def fetch_tvl(chain_id, address):
    """
    Fetch total value locked (TVL) using Covalent API for a given address on a chain.
    """
    url = f"https://api.covalenthq.com/v1/{chain_id}/address/{address}/balances_v2/"
    params = {
        "key": COVALENT_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    tvl = 0
    for item in data.get("data", {}).get("items", []):
        quote = item.get("quote", 0)
        if quote:
            tvl += quote
    return round(tvl, 2)

# ----------------------------
# 2. Fetch Token Info via CoinGecko
# ----------------------------
def fetch_token_info(token_id):
    """
    Fetch token metrics like market cap, supply, and community size.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "name": data["name"],
        "market_cap": data["market_data"]["market_cap"]["usd"],
        "circulating_supply": data["market_data"]["circulating_supply"],
        "twitter_followers": data["community_data"]["twitter_followers"]
    }
