from utils import get_db_engine
import pandas as pd

engine = get_db_engine()

print("Loading player IDs from matches...")
match_df = pd.read_sql("SELECT player1_id, player2_id, winner_id FROM matches", engine)

# Flatten and deduplicate player IDs
player_ids = pd.unique(match_df[['player1_id', 'player2_id', 'winner_id']].values.ravel('K'))
player_ids = [pid for pid in player_ids if pid]  # remove None

# Create placeholder player records
players = [{'player_id': pid, 'name': None, 'nationality': None, 'ranking': None} for pid in player_ids]
df = pd.DataFrame(players)

# Remove already existing players
try:
    existing_ids = pd.read_sql("SELECT player_id FROM players", engine)['player_id'].tolist()
    df = df[~df['player_id'].isin(existing_ids)]
except Exception as e:
    print(f"⚠️ Could not fetch existing player IDs: {e}")

# Insert new players
try:
    df.to_sql('players', engine, if_exists='append', index=False)
    print(f"✅ Inserted {len(df)} placeholder players.")
except Exception as e:
    print(f"❌ Error inserting players: {e}")