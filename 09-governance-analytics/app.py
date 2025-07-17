import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from snapshot_utils import get_snapshot_data
from governance_score import score_dao_governance

st.set_page_config(page_title="DAO Governance Tracker", layout="wide")
st.title("🗳️ DAO Governance Activity Tracker")

st.markdown("""
Track governance activity using **Snapshot**.  
Enter your DAO Snapshot Space ID below:
""")

dao_snapshot = st.text_input("Snapshot Space ID", value="uniswap.eth")

snapshot_df = pd.DataFrame()
if dao_snapshot:
    with st.spinner("Fetching Snapshot proposals..."):
        snapshot_df = get_snapshot_data(dao_snapshot.strip())

# Score only based on Snapshot
scores = score_dao_governance(snapshot_df)

st.subheader("📊 Governance Scorecard")
cols = st.columns(3)
cols[0].metric("Snapshot Proposals", scores["Snapshot Proposals"])
cols[1].metric("Avg Snapshot Votes", scores["Avg Votes per Proposal"])
cols[2].metric("Snapshot Pass Rate", scores["Snapshot Proposal Pass Rate"])

st.subheader("📄 Snapshot Proposals")
if not snapshot_df.empty:
    st.dataframe(snapshot_df[["title", "state", "votes", "scores_total", "created"]], use_container_width=True)
else:
    st.info("No Snapshot proposals found. Please check your Snapshot Space ID (e.g., `uniswap.eth`).")

if not snapshot_df.empty:
    st.subheader("📈 Snapshot Proposal Trend")
    trend = pd.to_datetime(snapshot_df["created"], unit="s").dt.date
    counts = trend.value_counts().sort_index()
    fig, ax = plt.subplots()
    counts.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_xlabel("Date")
    ax.set_ylabel("Proposals")
    st.pyplot(fig)

st.markdown("---")
st.caption("Built with ❤️ by Objemmanuel · Powered by Snapshot")
