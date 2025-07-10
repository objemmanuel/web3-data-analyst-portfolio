import requests
import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────────────
# 🔑 Load your Etherscan API key from Streamlit secrets
# Make sure to set ETHERSCAN_API_KEY in .streamlit/secrets.toml
# ─────────────────────────────────────────────────────────────
ETHERSCAN_API_KEY = st.secrets["ETHERSCAN_API_KEY"]

# ─────────────────────────────────────────────────────────────
# 📥 Fetch all normal transactions related to a smart contract
# - contract_address: Ethereum address of the smart contract
# - start_block/end_block: Block range to search (defaults to full history)
# Returns a cleaned Pandas DataFrame
# ─────────────────────────────────────────────────────────────
def fetch_contract_transactions(contract_address, start_block=0, end_block=99999999):
    url = "https://api.etherscan.io/api"

    params = {
        "module": "account",
        "action": "txlist",
        "address": contract_address,
        "startblock": start_block,
        "endblock": end_block,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        result = response.json()

        # ✅ Etherscan response with status code "1" means success
        if result["status"] == "1":
            df = pd.DataFrame(result["result"])
            return df
        else:
            # ⚠️ If status is "0", return empty DataFrame
            st.error(f"⚠️ Etherscan Error: {result.get('message', 'No message returned')}")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"🚨 Exception while calling Etherscan API: {e}")
        return pd.DataFrame()
