import streamlit as st
import pandas as pd
import plotly.express as px
from api_utils import fetch_contract_transactions

# ─────────────────────────────────────────────────────────────
# ✅ Streamlit Page Setup
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Contract Interaction Analyzer",
    layout="wide"
)
st.title("📜 Smart Contract Interaction Analyzer")
st.markdown("Analyze smart contract usage: transactions, gas usage, top wallets, and more.")

# ─────────────────────────────────────────────────────────────
# 🧾 Contract Address Input
# ─────────────────────────────────────────────────────────────
contract_address = st.text_input(
    "Enter Smart Contract Address (Ethereum):",
    value="0x5f65f7b609678448494de4c87521cdf6cef1e932"  # Example: Aave contract
)

# ─────────────────────────────────────────────────────────────
# 🔍 Fetch and Process Contract Transactions
# ─────────────────────────────────────────────────────────────
if contract_address:
    with st.spinner("Fetching data from Etherscan..."):
        df = fetch_contract_transactions(contract_address)

    if df.empty:
        st.warning("⚠️ No transaction data found. Check the address or try another.")
    else:
        # Convert timestamps and ensure proper numeric types
        df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')
        df['gasUsed'] = pd.to_numeric(df['gasUsed'], errors='coerce')
        df['from'] = df['from'].str.lower()
        df['to'] = df['to'].str.lower()
        contract_address_lower = contract_address.lower()

        # ─────────────────────────────────────────────
        # 📊 Summary Stats
        # ─────────────────────────────────────────────
        st.subheader("📊 Quick Stats")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Transactions", len(df))
        col2.metric("Unique Wallets", df['from'].nunique())
        col3.metric("Average Gas Used", f"{df['gasUsed'].mean():,.0f}")
        col4.metric("Contract Calls", df[df['to'] == contract_address_lower].shape[0])

        # ─────────────────────────────────────────────
        # 📈 Daily Transaction Volume Chart
        # ─────────────────────────────────────────────
        st.subheader("📈 Transactions Over Time")
        tx_by_day = df.groupby(df['timeStamp'].dt.date).size().reset_index(name='tx_count')
        fig = px.line(tx_by_day, x='timeStamp', y='tx_count', title="Daily Transaction Count")
        st.plotly_chart(fig, use_container_width=True)

        # ─────────────────────────────────────────────
        # 🧠 Top Interacting Wallets Table
        # ─────────────────────────────────────────────
        st.subheader("🧠 Top Interacting Wallets")
        top_wallets = df['from'].value_counts().head(10).reset_index()
        top_wallets.columns = ['Wallet Address', 'Transaction Count']
        st.dataframe(top_wallets, use_container_width=True)
