import streamlit as st
import pandas as pd
import plotly.express as px
import json
from api_utils import (
    get_nft_collection_info,
    get_nft_transfers,
    get_token_metadata
)

# ---------------------- Streamlit Setup ----------------------
st.set_page_config(page_title="NFT Dashboard", layout="wide")
st.title("🖼️ NFT Collection Analytics Dashboard")

# ---------------------- User Input ----------------------
contract_address = st.text_input(
    "Enter NFT Contract Address",
    "0xbd3531da5cf5857e7cfaa92426877b022e612cf8"  # Pudgy Penguins
)

# ---------------------- Load Data ----------------------
if contract_address:
    metadata = get_nft_collection_info(contract_address)
    transfers = get_nft_transfers(contract_address)

    # ---------------------- Show Metadata ----------------------
    if "error" in metadata:
        st.error(f"Failed to load metadata: {metadata['error']}")
    else:
        st.subheader("📦 Collection Metadata")
        st.json(metadata)

    # ---------------------- Transfers ----------------------
    if transfers:
        df = pd.DataFrame(transfers)
        df["block_timestamp"] = pd.to_datetime(df["block_timestamp"])
        df["date"] = df["block_timestamp"].dt.date

        st.subheader("🔁 Recent Transfers")
        st.dataframe(df[["block_timestamp", "token_id", "from_address", "to_address"]])

        # Transfer volume chart
        st.subheader("📈 Daily Transfer Volume")
        volume = df.groupby("date").size().reset_index(name="transfer_count")
        fig = px.bar(volume, x="date", y="transfer_count", title="Transfers per Day")
        st.plotly_chart(fig, use_container_width=True)

        # Whale wallets
        st.subheader("🐋 Top Wallets")
        col1, col2 = st.columns(2)

        senders = df["from_address"].value_counts().head(10).reset_index()
        senders.columns = ["Wallet", "Sent"]

        receivers = df["to_address"].value_counts().head(10).reset_index()
        receivers.columns = ["Wallet", "Received"]

        with col1:
            st.markdown("### 🔼 Top Senders")
            st.dataframe(senders)
        with col2:
            st.markdown("### 🔽 Top Receivers")
            st.dataframe(receivers)
    else:
        st.warning("No recent transfer data found.")

    # ---------------------- Trait & Rarity Analysis ----------------------
    st.subheader("🧬 Trait Frequency Analysis")

    nfts = get_token_metadata(contract_address)
    all_traits = []

    for nft in nfts:
        meta = nft.get("metadata")
        if meta:
            try:
                parsed = json.loads(meta)
                attributes = parsed.get("attributes", [])
                if isinstance(attributes, list):
                    for attr in attributes:
                        t_type = attr.get("trait_type")
                        value = attr.get("value")
                        if t_type and value:
                            all_traits.append((t_type, value))
            except json.JSONDecodeError:
                continue

    if all_traits:
        trait_df = pd.DataFrame(all_traits, columns=["Trait Type", "Value"])
        trait_summary = trait_df.groupby(["Trait Type", "Value"]).size().reset_index(name="Count")

        fig2 = px.bar(
            trait_summary,
            x="Value",
            y="Count",
            color="Trait Type",
            title="📊 NFT Trait Frequency",
            labels={"Value": "Trait", "Count": "Frequency"},
            height=500
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No traits found to analyze.")

    