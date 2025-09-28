import os
import time
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# Load environment variables
load_dotenv()

API_KEY = os.getenv('SPORTRADAR_API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'tennis_db')

def get_db_engine():
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, echo=False)

def safe_get(url, params=None, max_retries=3, backoff=2):
    if params is None:
        params = {}
    params['api_key'] = API_KEY

    for i in range(max_retries):
        try:
            r = requests.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 429:
                wait = backoff * (i + 1)
                print(f"Rate limited. Sleeping {wait}s")
                time.sleep(wait)
            else:
                r.raise_for_status()
        except Exception as e:
            print("Request error:", e)
            time.sleep(backoff * (i+1))
    raise RuntimeError("Failed to fetch data")

def df_to_sql(df: pd.DataFrame, table_name: str, engine, if_exists='append'):
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
