import os
import requests
import json

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def save_summary(source: str, input_text: str, summary: str, user_id: str | None = None, meta: dict | None = None):
    """
    Store a summary in Supabase 'summaries' table.
    Logs clearly on Render so we can debug.
    """

    # Basic sanity logs
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("save_summary: missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY, skipping insert")
        return

    # Ensure base URL has no trailing slash
    base_url = SUPABASE_URL.rstrip("/")

    table_url = f"{base_url}/rest/v1/summaries"

    payload = {
        "user_id": user_id or "anonymous",
        "source": source,
        "input_text": (input_text or "")[:8000],
        "summary": (summary or "")[:8000],
        "meta": meta or {},
    }

    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    try:
        print("save_summary: POST", table_url, "payload keys:", list(payload.keys()))
        resp = requests.post(table_url, headers=headers, data=json.dumps(payload), timeout=10)
        if resp.ok:
            print("save_summary: inserted OK, status", resp.status_code)
        else:
            print("save_summary: Supabase error", resp.status_code, resp.text)
    except Exception as e:
        print("save_summary: exception", repr(e))

