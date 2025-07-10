# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from api_utils import fetch_token_transfers

st.set_page_config(page_title="Token Flow & Whale Tracker", layout="wide")

st.title("🕸️ Token Flow & Whale Tracker")

# Input: Token contract address
contract_address = st.text_input(
    "Enter ERC-20 Token Contract Address",
    value="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC default
)

# Threshold input for large transfers
threshold = st.slider("🚨 Set Large Transfer Alert Threshold", 10_000, 10_000_000, 1_000_000)

if contract_address:
    # Fetch data from Etherscan API
    df = fetch_token_transfers(contract_address)

    if not df.empty:
        st.success(f"✅ Fetched {len(df)} transfer records")

        # Display raw data
        with st.expander("📄 View Raw Data"):
            st.dataframe(df[["from", "to", "value", "timeStamp"]])

        # Convert 'value' to human-readable format (from Wei)
        df["value"] = df["value"].astype(float) / (10 ** 6)

        # 🚨 Detect Large Transfers
        st.subheader("🚨 Large Transfers Alert")
        large_txns = df[df["value"] > threshold]

        if not large_txns.empty:
            st.dataframe(large_txns[["from", "to", "value", "timeStamp"]])
        else:
            st.info("No large transfers detected above the selected threshold.")

        # 🧠 Whale Analysis
        top_addresses = df.groupby("from")["value"].sum().sort_values(ascending=False).head(10)
        st.subheader("🐋 Top Whale Addresses by Outflow")
        st.dataframe(top_addresses)

        # 🌐 Token Flow Graph (Sankey)
        st.subheader("🔄 Token Flow Diagram")

        # Build graph
        G = nx.DiGraph()
        for _, row in df.iterrows():
            sender = row["from"]
            receiver = row["to"]
            value = row["value"]

            if G.has_edge(sender, receiver):
                G[sender][receiver]["weight"] += value
            else:
                G.add_edge(sender, receiver, weight=value)

        # Prepare address index mapping
        address_list = list(set(df["from"].tolist() + df["to"].tolist()))
        address_index = {addr: i for i, addr in enumerate(address_list)}

        # Use only a subset for clean visual
        sankey_data = df.head(100)

        sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=[addr[:8] + "..." for addr in address_list]
            ),
            link=dict(
                source=[address_index[row["from"]] for _, row in sankey_data.iterrows()],
                target=[address_index[row["to"]] for _, row in sankey_data.iterrows()],
                value=[row["value"] for _, row in sankey_data.iterrows()]
            )
        )])

        st.plotly_chart(sankey, use_container_width=True)

    else:
        st.warning("⚠️ No data found for this token contract.")
