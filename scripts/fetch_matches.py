import os
import pandas as pd
from dotenv import load_dotenv
from utils import get_db_engine, safe_get

# Load API key
load_dotenv()
API_KEY = os.getenv("SPORTRADAR_API_KEY")
BASE = f"https://api.sportradar.com/tennis/trial/v3/en"

# Database engine
engine = get_db_engine()

print("Fetching matches via daily schedule...")

# Fixed date (trial known working)
date_str = "2023-06-10"
url = f"{BASE}/schedules/{date_str}/summaries.json"

resp = safe_get(url)

if resp is not None:
    schedules = resp.get("summaries", [])
    print(f"Found {len(schedules)} matches")

    matches_data = []

    for match in schedules:
        sport_event = match.get("sport_event", {})
        match_id = sport_event.get("id")
        competition = sport_event.get("competition", {})
        venue = sport_event.get("venue", {})

        competitors = sport_event.get("competitors", [])
        player1_id = competitors[0]["id"] if len(competitors) > 0 else None
        player2_id = competitors[1]["id"] if len(competitors) > 1 else None

        matches_data.append({
            "match_id": match_id,
            "competition_id": competition.get("id"),
            "venue_id": venue.get("id"),
            "player1_id": player1_id,
            "player2_id": player2_id,
            "scheduled": sport_event.get("start_time"),
            "status": sport_event.get("status", "scheduled"),
            "winner_id": None  # can be updated later
        })

    if matches_data:
        df = pd.DataFrame(matches_data).drop_duplicates(subset=["match_id"])
        print(df.head())
        df.to_sql("matches", engine, if_exists="append", index=False)
        print(f"✅ {len(df)} matches saved to DB")
    else:
        print("⚠️ No matches found in summaries")
else:
    print("❌ Failed to fetch data")
