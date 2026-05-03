import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")  
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials")

BASE_URL = f"{SUPABASE_URL}/rest/v1"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def add_stock(ticker):
    try:
        payload = {
            "ticker": ticker.upper(),
            "active": 1
        }

        res = requests.post(
            f"{BASE_URL}/portfolio",
            headers=HEADERS,
            json=payload
        )

        return res.status_code in [200, 201]

    except Exception as e:
        print("add_stock error:", e)
        return False
    
def remove_stock(ticker):
    try:
        ticker = ticker.strip().upper()

        res = requests.delete(
            f"{BASE_URL}/portfolio",
            headers=HEADERS,
            params={"ticker": f"eq.{ticker}"}
        )

        return res.status_code in [200, 204]

    except Exception as e:
        print("remove_stock error:", e)
        return False
    
def get_portfolio():
    try:
        res = requests.get(
            f"{BASE_URL}/portfolio",
            headers=HEADERS,
            params={
                "select": "ticker",
                "active": "eq.1"
            }
        )

        if res.status_code != 200:
            return []

        data = res.json()
        return [row["ticker"] for row in data]

    except Exception as e:
        print("get_portfolio error:", e)
        return []

def save_daily_stock_data(df_raw, date=None):
    try:
        if df_raw is None or df_raw.empty:
            return False

        date = date or datetime.utcnow().date().isoformat()

        records = []

        for _, row in df_raw.iterrows():
            records.append({
                "ticker": row["symbol"].upper(),
                "date": date,
                "close_price": float(row["today_close"]),
                "price_change_pct": float(row["percent_price_change"]),
                "volume_change_pct": float(row["percent_volume_change"])
            })

        res = requests.post(
            f"{BASE_URL}/daily_stock_data",
            headers=HEADERS,
            json=records
        )

        return res.status_code in [200, 201]

    except Exception as e:
        print("save_daily_stock_data error:", e)
        return False