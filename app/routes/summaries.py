from fastapi import APIRouter
import os, requests

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

@router.get("/summaries")
def get_summaries():
    url = f"{SUPABASE_URL}/rest/v1/summaries?select=*"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

