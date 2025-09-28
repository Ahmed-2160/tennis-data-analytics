from utils import safe_get, get_db_engine
import pandas as pd

# Base URL and DB engine
BASE = 'https://api.sportradar.com/tennis/trial/v3/en'
engine = get_db_engine()

print("📡 Fetching competitions...")
resp = safe_get(f"{BASE}/competitions.json")
competitions = resp.get('competitions', [])

# Normalize JSON into DataFrame
comp_df = pd.json_normalize(competitions)

# Rename columns to match MySQL schema
comp_df = comp_df.rename(columns={
    'id': 'competition_id',
    'name': 'name',  # match DB column name
    'parent_id': 'parent_id',
    'type': 'type',
    'gender': 'gender',
    'category.id': 'category_id',
    'category.name': 'category_name'
})

# Select relevant columns
comp_df = comp_df[['competition_id', 'name', 'parent_id', 'type', 'gender', 'category_id', 'category_name']]

# Extract unique categories
cats = comp_df[['category_id', 'category_name']].drop_duplicates().dropna()

print("🗃️ Writing categories to DB...")
cats.to_sql('categories', engine, if_exists='append', index=False)

print("🗃️ Writing competitions to DB...")
comp_df.drop(columns=['category_name'], inplace=True)
comp_df.to_sql('competitions', engine, if_exists='append', index=False)

print("✅ Done: categories & competitions loaded successfully.")