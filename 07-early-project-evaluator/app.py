# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from api_utils import get_token_metrics_from_coingecko
from scoring_utils import calculate_score

# -----------------------------------
# 🎨 Streamlit Page Config
# -----------------------------------
st.set_page_config(page_title="Early-Stage Web3 Project Evaluator", layout="wide")

st.title("🧠 Early-Stage Web3 Project Evaluator")
st.markdown("Analyze any Web3/NFT/DeFi token based on real tokenomics and on-chain metrics.")

st.markdown("---")

# -----------------------------------
# 🧾 User Input
# -----------------------------------
token_id = st.text_input("Enter Token ID (as listed on CoinGecko)", value="uniswap")

if st.button("🔍 Analyze Token"):
    st.info("⏳ Fetching data from CoinGecko...")

    metrics, error = get_token_metrics_from_coingecko(token_id)

    if error:
        st.error(error)
    else:
        # --------------------------
        # 📊 Display Raw Metrics
        # --------------------------
        st.subheader("📊 Key Metrics")
        df_metrics = pd.DataFrame([metrics]).T.rename(columns={0: "Value"})
        st.dataframe(df_metrics)

        # --------------------------
        # ✅ Scoring
        # --------------------------
        score, score_breakdown = calculate_score(metrics)

        st.subheader("✅ Project Score")
        st.metric(label="Score (0–100)", value=round(score, 2))

        # Bar chart of score breakdown
        st.subheader("📈 Score Breakdown")
        fig = px.bar(
            x=list(score_breakdown.keys()),
            y=list(score_breakdown.values()),
            labels={"x": "Metric", "y": "Score"},
            title="Scoring Breakdown (Per Metric)"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Recommendation
        st.markdown("---")
        if score > 75:
            st.success("🔥 Strong fundamentals. Likely a good project to invest in.")
        elif score > 50:
            st.warning("⚠️ Moderate performance. More research needed.")
        else:
            st.error("❌ Weak fundamentals. Be cautious before investing.")

        # Export
        with st.expander("📁 Export Metrics as CSV"):
            csv = pd.DataFrame([metrics]).to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", data=csv, file_name=f"{token_id}_metrics.csv")
