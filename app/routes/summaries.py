kfrom fastapi import APIRouter
import os
import requests

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


@router.get("/summaries")
def get_summaries():
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        return {"error": "Supabase not configured"}

    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/summaries?select=*"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    # If Supabase errors, just return its message so we can see it
    try:
        data = resp.json()
    except Exception:
        data = resp.text
    return data

