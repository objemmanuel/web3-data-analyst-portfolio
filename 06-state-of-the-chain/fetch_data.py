import requests         # For sending HTTP requests to APIs
import json             # To save and load JSON data
import os               # To create folders and handle paths
from datetime import datetime  # For timestamping

# Create the 'data' folder if it doesn't already exist
os.makedirs("data", exist_ok=True)

# Utility function to save any dictionary as a JSON file
def save_json(data, filename):
    with open(f"data/{filename}.json", "w") as f:
        json.dump(data, f, indent=2)

# Function to fetch Ethereum fee summary from DeFiLlama API
def fetch_defillama_tvl():
    url = "https://api.llama.fi/summary/fees/ethereum"
    res = requests.get(url)
    
    if res.status_code == 200:
        data = res.json()
        save_json(data, "ethereum_fees")  # Save as ethereum_fees.json
        print("✅ Ethereum fees saved.")
    else:
        print("❌ Failed to fetch Ethereum fee data")

# Function to fetch top 10 tokens by market cap from CoinGecko API
def fetch_coingecko_token_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",                 # Get prices in USD
        "order": "market_cap_desc",           # Order by largest market cap
        "per_page": 10,                       # Top 10 tokens
        "page": 1,
        "sparkline": False                    # No historical sparkline data
    }

    res = requests.get(url, params=params)
    
    if res.status_code == 200:
        data = res.json()
        save_json(data, "top_tokens")         # Save as top_tokens.json
        print("✅ Token data saved.")
    else:
        print("❌ Failed to fetch token data")

# Main function to call both data fetching functions
def main():
    print(f"⏳ Fetching data... {datetime.now()}")
    
    fetch_defillama_tvl()
    fetch_coingecko_token_data()
    
    print(f"✅ Done fetching at {datetime.now()}")

# Run the script if this file is executed directly
if __name__ == "__main__":
    main()
