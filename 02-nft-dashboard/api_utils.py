import requests
import os

# Set your Moralis API Key here
MORALIS_API_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImYyNmRlYzY1LWRmNjUtNDBlYS1hMDU1LTlhMDg3MzdmZmRjMCIsIm9yZ0lkIjoiNDU4NDQ1IiwidXNlcklkIjoiNDcxNjYxIiwidHlwZUlkIjoiYjRiNmZjOWQtOTZkYy00YmZiLWIwN2ItZDA1YWVkNWE1Y2IwIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NTIwOTA1NDksImV4cCI6NDkwNzg1MDU0OX0.v475KNgWLagX-sRRc-i1zwS_ytLSkSgx9RxbDtSN96o") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImYyNmRlYzY1LWRmNjUtNDBlYS1hMDU1LTlhMDg3MzdmZmRjMCIsIm9yZ0lkIjoiNDU4NDQ1IiwidXNlcklkIjoiNDcxNjYxIiwidHlwZUlkIjoiYjRiNmZjOWQtOTZkYy00YmZiLWIwN2ItZDA1YWVkNWE1Y2IwIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NTIwOTA1NDksImV4cCI6NDkwNzg1MDU0OX0.v475KNgWLagX-sRRc-i1zwS_ytLSkSgx9RxbDtSN96o"

def get_nft_collection_info(contract_address, chain="eth"):
    url = f"https://deep-index.moralis.io/api/v2/nft/{contract_address}/metadata"
    headers = {
        "X-API-Key": MORALIS_API_KEY,
        "accept": "application/json"
    }
    params = {"chain": chain}

    try:
        res = requests.get(url, headers=headers, params=params)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def get_nft_transfers(contract_address, chain="eth", limit=50):
    url = f"https://deep-index.moralis.io/api/v2/nft/{contract_address}/transfers"
    headers = {
        "X-API-Key": MORALIS_API_KEY,
        "accept": "application/json"
    }
    params = {"chain": chain, "format": "decimal", "limit": limit}

    try:
        res = requests.get(url, headers=headers, params=params)
        return res.json().get("result", [])
    except Exception as e:
        return []

def get_token_metadata(contract_address, chain="eth", limit=50):
    url = f"https://deep-index.moralis.io/api/v2/nft/{contract_address}"
    headers = {
        "X-API-Key": MORALIS_API_KEY,
        "accept": "application/json"
    }
    params = {"chain": chain, "format": "json", "limit": limit}

    try:
        res = requests.get(url, headers=headers, params=params)
        return res.json().get("result", [])
    except Exception as e:
        return []
