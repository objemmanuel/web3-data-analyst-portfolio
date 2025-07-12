# scoring_utils.py

def calculate_score(metrics):
    """
    Calculate an overall project score out of 100 based on key metrics.
    Metrics include DAU, market cap, volume, whale/comm holder %, tokenomics.
    """
    detailed_scores = {}

    try:
        # 1. Daily Active Users (DAU) - scaled to 5,000 max
        dau = metrics.get("Estimated DAU", 0)
        detailed_scores["DAU"] = min(dau / 5000, 1) * 100

        # 2. Whale Concentration (lower is better)
        whale_pct = metrics.get("Whale Holders % (est)", 20)
        detailed_scores["Whale Concentration"] = max((20 - whale_pct) / 20, 0) * 100

        # 3. Community Holders (higher is better)
        community_pct = metrics.get("Community Holders % (est)", 80)
        detailed_scores["Community Distribution"] = min(community_pct / 100, 1) * 100

        # 4. Market Cap Score - scaled to 1B USD
        market_cap = metrics.get("Market Cap (USD)", 0)
        detailed_scores["Market Cap"] = min(market_cap / 1_000_000_000, 1) * 100

        # 5. 24h Trading Volume - scaled to $100M
        volume = metrics.get("24h Trading Volume (USD)", 0)
        detailed_scores["Liquidity (Volume)"] = min(volume / 100_000_000, 1) * 100

        # 6. Tokenomics - Circulating / Total Supply
        circ = metrics.get("Circulating Supply", 0)
        total = metrics.get("Total Supply", 1)
        tokenomics_ratio = min(circ / total, 1) if total else 0
        detailed_scores["Tokenomics Health"] = tokenomics_ratio * 100

        # Final Average Score
        total_score = sum(detailed_scores.values()) / len(detailed_scores)
        return total_score, detailed_scores

    except Exception as e:
        return 0, {"Error": str(e)}
