import requests

# You can get an API key from https://beaconcha.in/api/v1/docs
BEACONCHAIN_API_KEY = "Yjc0cXpETHE5V3VjSk1SbDlueHhWUEpEcjVoaA"
BEACONCHAIN_BASE_URL = "https://beaconcha.in/api/v1"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "apikey": BEACONCHAIN_API_KEY
}

def get_validator_info(pubkey):
    url = f"{BEACONCHAIN_BASE_URL}/validator/{pubkey}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json().get("data", {})
    print(f"[BeaconChain] Validator info error: {res.text}")
    return {}

def get_validator_performance(pubkey):
    url = f"{BEACONCHAIN_BASE_URL}/validator/performance/{pubkey}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json().get("data", {})
    print(f"[BeaconChain] Performance error: {res.text}")
    return {}

def get_eth_network_overview():
    url = f"{BEACONCHAIN_BASE_URL}/epoch/latest"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json().get("data", {})
    print(f"[BeaconChain] Epoch overview error: {res.text}")
    return {}

def get_all_eth_overview(pubkey):
    info = get_validator_info(pubkey)
    perf = get_validator_performance(pubkey)
    net = get_eth_network_overview()

    return {
        "validator_info": info,
        "performance": perf,
        "network": net
    }
