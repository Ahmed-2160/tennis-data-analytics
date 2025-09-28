import os
import pandas as pd
from utils import safe_get, get_db_engine
from dotenv import load_dotenv
from datetime import date

# Load API key
load_dotenv()
API_KEY = os.getenv("SPORTRADAR_API_KEY")
BASE = f"https://api.sportradar.com/tennis/trial/v3/en"

# Database engine
engine = get_db_engine()

print("Fetching players via daily schedule...")

# Use today's date (you can change if needed)
today = "2023-07-15"   # <-- pick a recent date
url = f"{BASE}/schedules/{today}/summaries.json"

resp = safe_get(url)

if resp is not None:
    schedules = resp.get("summaries", [])
    players_data = []

    for match in schedules:
        competitors = match.get("competitors", [])
        for comp in competitors:
            players_data.append({
                "player_id": comp["id"],
                "name": comp["name"],
                "nationality": comp.get("country", None),
                "ranking": None
            })

    if players_data:
        df = pd.DataFrame(players_data).drop_duplicates(subset=["player_id"])
        print(df.head())
        df.to_sql("players", engine, if_exists="append", index=False)
        print(f"✅ {len(df)} players saved to DB")
    else:
        print("⚠️ No players found for {today}")
else:
    print("❌ Failed to fetch data")
