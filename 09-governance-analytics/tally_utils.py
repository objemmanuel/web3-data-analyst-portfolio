# tally_utils.py

import requests
import pandas as pd

TALLY_API_KEY = "933e4cca1dc09d5ef5aca17ec8d06fbd5d69940f7170c79867c277a12cbbcf88"  # Replace with your real API key
TALLY_ENDPOINT = "https://api.tally.xyz/query"

def get_tally_data(dao_slug):
    query = """
    query Proposals($slug: String!) {
      organization(slug: $slug) {
        proposals {
          edges {
            node {
              title
              status
              votes {
                abstain
                against
                for
              }
            }
          }
        }
      }
    }
    """

    variables = {"slug": dao_slug}
    headers = {
        "Content-Type": "application/json",
        "Api-Key": TALLY_API_KEY
    }

    try:
        response = requests.post(
            TALLY_ENDPOINT,
            json={"query": query, "variables": variables},
            headers=headers
        )

        if response.status_code != 200:
            print(f"[Tally] Error {response.status_code} — {response.text}")
            return pd.DataFrame()

        data = response.json()
        proposals = data.get("data", {}).get("organization", {}).get("proposals", {}).get("edges", [])

        rows = []
        for edge in proposals:
            p = edge["node"]
            votes = p.get("votes", {})
            rows.append({
                "title": p["title"],
                "status": p["status"],
                "votes_total": sum(votes.values()),
                "votes_yes": votes.get("for", 0),
                "votes_no": votes.get("against", 0),
                "votes_abstain": votes.get("abstain", 0),
            })

        return pd.DataFrame(rows)

    except Exception as e:
        print(f"[Tally] Exception: {e}")
        return pd.DataFrame()
