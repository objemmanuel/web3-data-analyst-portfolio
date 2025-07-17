import requests
import pandas as pd

SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"


def get_validator_data():
    """Fetch all validator data from Solana mainnet."""
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getVoteAccounts"
    }

    response = requests.post(SOLANA_RPC_URL, json=payload, headers=headers)
    result = response.json()

    if "result" in result:
        return result["result"]
    else:
        raise ValueError("Failed to fetch validator data from Solana")


def process_validators_data():
    """Process validators into a DataFrame with staking stats."""
    data = get_validator_data()
    current_validators = data.get("current", [])
    delinquent_validators = data.get("delinquent", [])

    all_validators = current_validators + delinquent_validators

    df = pd.DataFrame(all_validators)
    df["stake_lamports"] = pd.to_numeric(df["activatedStake"], errors='coerce')
    df["stake_sol"] = df["stake_lamports"] / 1e9
    df["commission"] = pd.to_numeric(df["commission"], errors='coerce')
    df["is_delinquent"] = df["votePubkey"].isin([v["votePubkey"] for v in delinquent_validators])

    return df


def get_top_validators(df, top_n=10, sort_by="stake_sol"):
    """Get top N validators based on stake or performance."""
    top_validators = df.sort_values(by=sort_by, ascending=False).head(top_n)
    return top_validators


def get_summary_metrics(df):
    """Compute overall validator metrics like total stake, avg commission."""
    total_stake = df["stake_sol"].sum()
    avg_commission = df["commission"].mean()
    delinquent_count = df["is_delinquent"].sum()
    total_validators = len(df)

    return {
        "total_stake_sol": round(total_stake, 2),
        "average_commission_percent": round(avg_commission, 2),
        "delinquent_validators": delinquent_count,
        "total_validators": total_validators,
    }
