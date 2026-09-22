import requests
import json
import os

METABASE_URL = os.environ.get("METABASE_URL")
USERNAME = os.environ.get("METABASE_USER")
PASSWORD = os.environ.get("METABASE_PASS")

CARDS = {
    "iol": os.environ.get("CARD_IOL"),
    "not_racked": os.environ.get("CARD_NOT_RACKED"),
    "live_nf": os.environ.get("CARD_LIVE_NF"),
    "audit": os.environ.get("CARD_AUDIT"),
    "rackout": os.environ.get("CARD_RACKOUT")
}

def fetch_card_data(session_id, card_id):
    if not card_id:
        return []
    url = f"{METABASE_URL}/api/card/{card_id}/query"
    headers = {"X-Metabase-Session": session_id}
    res = requests.post(url, headers=headers)
    
    if res.status_code != 200:
        print(f"Failed to fetch card {card_id}")
        return []
        
    result = res.json()
    cols = [col["name"] for col in result["data"]["cols"]]
    rows = result["data"]["rows"]
    
    return [dict(zip(cols, row)) for row in rows]

def main():
    session_res = requests.post(
        f"{METABASE_URL}/api/session",
        json={"username": USERNAME, "password": PASSWORD}
    )
    session_res.raise_for_status()
    session_id = session_res.json()["id"]

    combined_data = {}
    for key, card_id in CARDS.items():
        print(f"Fetching {key} (Card ID: {card_id})...")
        combined_data[key] = fetch_card_data(session_id, card_id)

    with open("data.json", "w") as f:
        json.dump(combined_data, f, indent=2)

    print("data.json successfully updated!")

if __name__ == "__main__":
    main()
