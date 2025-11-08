import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def save_summary(source: str, input_text: str, summary: str, user_id: str | None = None, meta: dict | None = None):
    """Store a summary in Supabase. Fails silently if not configured."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        # Not configured; don't break the app
        print("save_summary: SUPABASE env vars missing, skipping.")
        return

    try:
        table_url = f"{SUPABASE_URL}/rest/v1/summaries"
        headers = {
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }
        payload = {
            "user_id": user_id,
            "source": source,
            "input_text": (input_text or "")[:8000],
            "summary": (summary or "")[:8000],
            "meta": meta or {},
        }
        resp = requests.post(table_url, headers=headers, json=payload, timeout=5)
        if not resp.ok:
            print("save_summary: Supabase error", resp.status_code, resp.text)
    except Exception as e:
        print("save_summary: exception", e)


