import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from solana_utils import (
    process_validators_data,
    get_top_validators,
    get_summary_metrics
)

from ethereum_utils import (
    get_all_eth_overview
)

# Set page config
st.set_page_config(page_title="Staking Analytics Dashboard", layout="wide")

# App Title
st.title("🔗 Web3 Staking Analytics Dashboard")

st.markdown("""
Welcome to the Web3 Staking Analytics Dashboard.

This dashboard provides real-time insights into validator performance for **Solana** and **Ethereum** networks.  
""")

# --- Tab layout ---
tab1, tab2 = st.tabs(["🌿 Solana Analytics", "🟣 Ethereum Analytics"])

# ======================================================
# 🌿 SOLANA TAB
# ======================================================
with tab1:
    st.header("📊 Solana Staking Analytics Dashboard")

    st.markdown("""
    This dashboard provides insights into Solana validator activity, including total stake, commission rates,
    and delinquent validators. The data is pulled in real-time from the Solana blockchain.
    """)

    # Fetch validator data
    with st.spinner("Fetching validator data from Solana..."):
        df_validators = process_validators_data()
        summary = get_summary_metrics(df_validators)

    # Display summary metrics
    st.subheader("🔢 Staking Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Stake (SOL)", f"{summary['total_stake_sol']:,}")
    col2.metric("Avg Commission (%)", f"{summary['average_commission_percent']}%")
    col3.metric("Total Validators", summary['total_validators'])
    col4.metric("Delinquent Validators", summary['delinquent_validators'])

    # Select Top N Validators
    st.subheader("🏆 Top Validators")
    top_n = st.slider("Select number of top validators to display:", min_value=5, max_value=30, value=10)

    top_validators = get_top_validators(df_validators, top_n=top_n)

    st.dataframe(
        top_validators[["votePubkey", "stake_sol", "commission", "is_delinquent"]],
        use_container_width=True,
        hide_index=True
    )

    # Stake Distribution Pie Chart
    st.subheader("📈 Stake Distribution (Top Validators)")
    fig, ax = plt.subplots()
    ax.pie(
        top_validators["stake_sol"],
        labels=[f"{vp[:4]}...{vp[-4:]}" for vp in top_validators["votePubkey"]],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

    # Commission Distribution
    st.subheader("📉 Commission Rates (Top Validators)")
    fig2, ax2 = plt.subplots()
    ax2.bar(
        [f"{vp[:4]}...{vp[-4:]}" for vp in top_validators["votePubkey"]],
        top_validators["commission"],
        color="orange"
    )
    ax2.set_ylabel("Commission (%)")
    ax2.set_xlabel("Validator")
    ax2.set_title("Commission Rates")
    st.pyplot(fig2)

    # Delinquent Validators
    st.subheader("🚨 Delinquent Validators")
    delinquents = df_validators[df_validators["is_delinquent"] == True]
    st.write(f"Number of delinquent validators: {len(delinquents)}")
    if not delinquents.empty:
        st.dataframe(
            delinquents[["votePubkey", "stake_sol", "commission"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("No delinquent validators at the moment 🎉")

# ======================================================
# 🟣 ETHEREUM TAB
# ======================================================
with tab2:
    st.header("🟣 Ethereum Staking Analytics")

    st.markdown("""
    Enter an Ethereum validator public key to fetch performance data from the BeaconChain API.
    """)

    eth_validator = st.text_input("Enter Ethereum Validator Public Key (BLS)", placeholder="Ex: 0x8c2...")

    if st.button("Analyze Ethereum Validator"):
        if eth_validator:
            with st.spinner("Fetching validator data from BeaconChain API..."):
                eth_data = get_all_eth_overview(eth_validator)

            if eth_data.get("validator_info"):
                st.success("✅ Ethereum validator data fetched successfully!")

                # Display validator info
                st.subheader("🧠 Validator Info")
                st.json(eth_data["validator_info"])

                st.subheader("📊 Performance")
                st.json(eth_data["performance"])

                st.subheader("🌐 Network Overview")
                st.json(eth_data["network"])

                # Optional metric display
                st.metric("Effective Balance (ETH)", eth_data["validator_info"].get("effectivebalance"))
                st.metric("Status", eth_data["validator_info"].get("status", "N/A"))

            else:
                st.warning("❌ Validator not found or API returned no data.")
        else:
            st.error("Please enter a valid Ethereum validator public key.")

# ======================================================
# Footer
# ======================================================
st.markdown("---")
st.caption("Built by Objemmanuel · Powered by Solana RPC, BeaconChain API, and Streamlit")
