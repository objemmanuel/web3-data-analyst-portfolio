import requests
import pandas as pd

def get_snapshot_data(space_id):
    url = "https://hub.snapshot.org/graphql"
    query = """
    query Proposals($space: String!) {
      proposals(first: 20, skip: 0, where: {space: $space}, orderBy: "created", orderDirection: desc) {
        id
        title
        body
        choices
        start
        end
        state
        scores
        scores_total
        votes
        created
      }
    }
    """

    variables = {"space": space_id}
    try:
        response = requests.post(url, json={"query": query, "variables": variables})
        data = response.json()

        if "errors" in data:
            print("[Snapshot] Error:", data["errors"])
            return pd.DataFrame()

        proposals = data["data"]["proposals"]
        df = pd.DataFrame(proposals)
        return df

    except Exception as e:
        print("[Snapshot] Exception:", e)
        return pd.DataFrame()
