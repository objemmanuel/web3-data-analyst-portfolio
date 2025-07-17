def normalize(value, max_val, min_val=0):
    """Normalize value to a score out of 100."""
    if value is None:
        return 0
    value = max(min(value, max_val), min_val)
    return ((value - min_val) / (max_val - min_val)) * 100


def score_ethereum_validator(summary, overview):
    perf = summary.get("performance", {})
    
    uptime_score = normalize(perf.get("attestationperformance"), 100)
    reward_score = normalize(summary.get("total_rewards_earned", 0), 5)  # max ~5 ETH rewards
    balance_score = normalize(summary.get("balance", 0), 32)
    apr_score = normalize(overview.get("apr_estimate", 0), 0.15, 0.02)  # APR between 2%-15%

    slashed_penalty = 0 if summary.get("slashed") else 100
    status_score = 100 if summary.get("status") == "active" else 50

    total_score = (
        0.4 * ((uptime_score + reward_score) / 2) +
        0.3 * balance_score +
        0.15 * slashed_penalty +
        0.15 * apr_score
    )

    return round(total_score, 2)


def score_solana_validator(validator):
    uptime_score = normalize(validator.get("uptime"), 100)
    success_score = normalize(validator.get("success_rate"), 100)
    commission_score = normalize(100 - validator.get("commission", 100), 100)
    active_stake_score = normalize(validator.get("active_stake", 0), 50_000_000)  # max ~50M SOL
    rewards_score = normalize(validator.get("rewards", 0), 1_000_000)

    slashed_penalty = 0 if validator.get("delinquent") else 100

    total_score = (
        0.4 * ((uptime_score + success_score) / 2) +
        0.3 * active_stake_score +
        0.15 * slashed_penalty +
        0.15 * ((commission_score + rewards_score) / 2)
    )

    return round(total_score, 2)
