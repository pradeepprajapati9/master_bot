"""Master Bot — access gate for workers.

Koi bhi module worker (YouTube, WhatsApp, ...) kaam karne se PEHLE ye check kare:
    "Is user ki profile approved hai? Aur ye module allowed + not-expired hai?"

Agar nahi -> kaam skip. Isse koi user seedhe DB me job daal ke bhi bina
permission kaam nahi karwa sakta.

Usage (worker me):
    from master_bot.worker.access_check import has_access
    if not has_access(user_id, "youtube"):
        continue   # ya job ko error/skipped mark kar do

Env chahiye (worker ke paas already hote hain):
    SUPABASE_URL, SUPABASE_SERVICE_KEY
"""
import os
from datetime import date

import requests

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
_H = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}


def _get(path, **params):
    r = requests.get(f"{SUPABASE_URL}/rest/v1/{path}", headers=_H, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def is_approved(user_id: str) -> bool:
    """User ki profile status == 'approved'?"""
    rows = _get("profiles", user_id=f"eq.{user_id}", select="status")
    return bool(rows) and rows[0].get("status") == "approved"


def has_access(user_id: str, module: str) -> bool:
    """True sirf tab jab: profile approved AND module allowed AND expiry nikli nahi."""
    if not is_approved(user_id):
        return False
    rows = _get("module_access",
                user_id=f"eq.{user_id}", module=f"eq.{module}",
                select="allowed,expiry")
    if not rows:
        return False
    a = rows[0]
    if not a.get("allowed"):
        return False
    exp = a.get("expiry")
    if exp and exp < date.today().isoformat():   # expiry date beet gayi
        return False
    return True


def allowed_user_ids(module: str) -> set:
    """Us module ke saare currently-allowed (approved + not expired) user_ids.
    enqueue step me useful — sirf inhi ke liye job banao."""
    today = date.today().isoformat()
    rows = _get("module_access", module=f"eq.{module}", allowed="eq.true",
                select="user_id,expiry")
    ids = {r["user_id"] for r in rows if not (r.get("expiry") and r["expiry"] < today)}
    if not ids:
        return set()
    # inme se sirf approved profiles rakho
    approved = _get("profiles", status="eq.approved", user_id=f"in.({','.join(ids)})",
                    select="user_id")
    return {p["user_id"] for p in approved}
