"""Reviews module — worker (sab jodta hai).

Har allowed user ke liye:
  1) access-gate check  (Master Bot: approved + 'reviews' allowed + not expired)
  2) auto_reply on hai?  connection + token hai?
  3) Google se naye reviews laao (jinka reply nahi diya + log me nahi)
  4) AI se reply banao (ai_reply) aur Google pe post karo
  5) reviews_log me record karo

GitHub Actions (schedule) pe chalega — youtube worker jaisa.
Env: SUPABASE_URL, SUPABASE_SERVICE_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GEMINI_API_KEY
"""
import os
import sys
import traceback

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

import requests

# master_bot/worker/access_check.py ko import karne ke liye (single repo)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from worker.access_check import has_access, allowed_user_ids   # noqa: E402

import config                 # noqa: E402
import ai_reply               # noqa: E402
import google_business as gb  # noqa: E402

SUPABASE_URL = config.SUPABASE_URL
SERVICE_KEY  = config.SUPABASE_SERVICE_KEY
_H = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}


def sb_get(path, **params):
    r = requests.get(f"{SUPABASE_URL}/rest/v1/{path}", headers=_H, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def sb_post(path, row):
    h = dict(_H, **{"Content-Type": "application/json", "Prefer": "return=minimal,resolution=merge-duplicates"})
    r = requests.post(f"{SUPABASE_URL}/rest/v1/{path}", headers=h, json=row, timeout=30)
    r.raise_for_status()


def process_user(uid: str):
    # gate: double-check (defence in depth)
    if not has_access(uid, config.MODULE):
        print(f"[skip] {uid[:8]} — access not allowed"); return

    settings = sb_get("reviews_settings", user_id=f"eq.{uid}",
                      select="business,tone,language,signature,auto_reply")
    if not settings or not settings[0].get("auto_reply"):
        print(f"[skip] {uid[:8]} — auto_reply off / no settings"); return
    s = settings[0]

    conn = sb_get("reviews_connections", user_id=f"eq.{uid}",
                  select="account_name,location_id,connected")
    tok  = sb_get("reviews_tokens", user_id=f"eq.{uid}", select="refresh_token")
    if not conn or not conn[0].get("connected") or not tok:
        print(f"[skip] {uid[:8]} — Google not connected"); return

    account_id  = conn[0]["account_name"]
    location_id = conn[0]["location_id"]

    access_token = gb.access_token_from_refresh(tok[0]["refresh_token"])
    reviews = gb.list_reviews(access_token, account_id, location_id)

    # already-handled review ids
    done = {r["review_id"] for r in sb_get("reviews_log", user_id=f"eq.{uid}", select="review_id")}

    replied = 0
    for rv in reviews:
        rid = rv.get("reviewId")
        if not rid or rid in done:
            continue
        if rv.get("reviewReply"):          # owner ne pehle se reply diya hai
            continue
        rating = gb.star_to_int(rv.get("starRating", ""))
        text   = rv.get("comment", "")

        reply = ai_reply.generate_reply(
            rating=rating, text=text,
            business=s.get("business") or "our business",
            tone=s.get("tone") or "friendly",
            language=s.get("language") or "English",
            signature=s.get("signature") or "",
        )
        try:
            gb.reply_to_review(access_token, account_id, location_id, rid, reply)
            status = "replied"; replied += 1
        except Exception as e:
            print(f"  reply fail {rid}: {e}"); status = "error"

        sb_post("reviews_log", {
            "user_id": uid, "review_id": rid, "rating": rating,
            "review_text": text, "reply_text": reply, "status": status,
        })
    print(f"[done] {uid[:8]} — {replied} new repl{'y' if replied==1 else 'ies'}")


def main():
    users = allowed_user_ids(config.MODULE)   # approved + 'reviews' allowed + not expired
    print(f"[reviews worker] {len(users)} allowed user(s)")
    for uid in users:
        try:
            process_user(uid)
        except Exception:
            print(f"[error] user {uid[:8]}:"); traceback.print_exc()


if __name__ == "__main__":
    main()
