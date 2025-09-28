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

print("Fetching venues via daily schedule...")

# Fixed date (trial known working)
date_str = "2023-06-10"
url = f"{BASE}/schedules/{date_str}/summaries.json"

resp = safe_get(url)

if resp is not None:
    schedules = resp.get("summaries", [])
    print(f"Found {len(schedules)} matches")

    venues_data = []

    for match in schedules:
        sport_event = match.get("sport_event", {})
        venue = sport_event.get("venue", None)
        if venue:
            venues_data.append({
                "venue_id": venue["id"],
                "name": venue["name"],
                "city": venue.get("city", None),
                "country": venue.get("country", None)
            })

    if venues_data:
        df = pd.DataFrame(venues_data).drop_duplicates(subset=["venue_id"])
        print(df.head())
        df.to_sql("venues", engine, if_exists="append", index=False)
        print(f"✅ {len(df)} venues saved to DB")
    else:
        print("⚠️ No venues found in summaries")
else:
    print("❌ Failed to fetch data")
