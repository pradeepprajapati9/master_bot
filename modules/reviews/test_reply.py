"""Local test — bina Google ke, sirf AI reply dekho.

Chalao:
    # (optional) asli AI ke liye pehle key set karo:
    #   Windows PowerShell:  $env:GEMINI_API_KEY="AIza..."
    # bina key ke bhi chalega — tab fallback reply dikhega.
    python test_reply.py
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")   # Windows console emoji fix
except Exception:
    pass

import ai_reply

SAMPLES = [
    (5, "Amazing food and super friendly staff, loved it!"),
    (4, "Good experience overall, will come again."),
    (2, "Waited 40 minutes and the order was cold."),
    (1, "Very rude behaviour, never coming back."),
    (5, ""),  # sirf rating, koi text nahi
]

print("=" * 60)
for rating, text in SAMPLES:
    reply = ai_reply.generate_reply(
        rating=rating, text=text,
        business="Sarvodaya Cafe", tone="friendly", language="English",
    )
    print(f"⭐ {rating}/5 | review: {text or '(no text)'}")
    print(f"🤖 reply : {reply}")
    print("-" * 60)
