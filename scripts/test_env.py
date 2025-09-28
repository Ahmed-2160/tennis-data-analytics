import os
from dotenv import load_dotenv

# Load .env from the same folder
load_dotenv()

api_key = os.getenv("SPORTRADAR_API_KEY")

if not api_key:
    raise RuntimeError("❌ API key not found. Check your .env file location and format.")
else:
    print("✅ API KEY loaded:", api_key[:6] + "..." + api_key[-4:])


