def score_dao_governance(snapshot_df):
    scores = {
        "Snapshot Proposals": 0,
        "Avg Votes per Proposal": 0,
        "Snapshot Proposal Pass Rate": "0%",
    }

    if snapshot_df is not None and not snapshot_df.empty:
        scores["Snapshot Proposals"] = len(snapshot_df)
        scores["Avg Votes per Proposal"] = round(snapshot_df["votes"].mean(), 2)
        passed = snapshot_df[snapshot_df["state"] == "closed"]
        pass_rate = (len(passed) / len(snapshot_df)) * 100 if len(snapshot_df) > 0 else 0
        scores["Snapshot Proposal Pass Rate"] = f"{pass_rate:.2f}%"

    return scores
