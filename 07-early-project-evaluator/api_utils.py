# api_utils.py

import requests

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_token_metrics_from_coingecko(token_id):
    """
    Fetch metrics from CoinGecko based only on token_id.
    No need for contract address anymore.
    """
    try:
        url = f"{COINGECKO_API}/coins/{token_id.lower()}"
        response = requests.get(url, params={
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false"
        })

        if response.status_code != 200:
            return None, f"CoinGecko Error: {response.json().get('error', 'Token not found.')}"

        data = response.json()
        market_data = data.get("market_data", {})

        # Fallbacks
        circ = market_data.get("circulating_supply") or 0
        total = market_data.get("total_supply") or 0

        # Estimate whale/community holders
        whale_pct = 15 if circ > 1_000_000 else 5
        community_pct = 100 - whale_pct

        metrics = {
            "Current Price (USD)": market_data.get("current_price", {}).get("usd"),
            "Market Cap (USD)": market_data.get("market_cap", {}).get("usd"),
            "Fully Diluted Valuation (USD)": market_data.get("fully_diluted_valuation", {}).get("usd"),
            "24h Trading Volume (USD)": market_data.get("total_volume", {}).get("usd"),
            "Circulating Supply": circ,
            "Total Supply": total,
            "Max Supply": market_data.get("max_supply") or 0,
            "All-Time High (ATH)": market_data.get("ath", {}).get("usd"),
            "All-Time Low (ATL)": market_data.get("atl", {}).get("usd"),
            "Estimated DAU": int(circ * 0.005),  # Assume 0.5% active daily
            "Whale Holders % (est)": whale_pct,
            "Community Holders % (est)": community_pct,
        }

        return metrics, None

    except Exception as e:
        return None, f"Exception: {str(e)}"
