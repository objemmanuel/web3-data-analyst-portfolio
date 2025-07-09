# api_utils.py

import requests

def get_uniswap_tvl():
    try:
        url = "https://api.llama.fi/tvl/uniswap"
        response = requests.get(url)
        if response.status_code == 200:
            raw = response.json()
            if isinstance(raw, (int, float)):
                return {"tvl": raw}
            return raw
        else:
            return {"error": f"Status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_uniswap_tvl_history():
    try:
        url = "https://api.llama.fi/protocol/uniswap"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("tvl", [])  # list of dicts with 'date' and 'totalLiquidityUSD'
        else:
            return []
    except Exception as e:
        return []
def get_token_price(symbol="uniswap"):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            market_data = data.get("market_data", {})
            return {
                "price": market_data.get("current_price", {}).get("usd"),
                "market_cap": market_data.get("market_cap", {}).get("usd"),
                "volume": market_data.get("total_volume", {}).get("usd"),
                "change_24h": market_data.get("price_change_percentage_24h"),
                "name": data.get("name", symbol.upper())
            }
        else:
            return {"error": f"Status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
