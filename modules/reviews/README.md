# ⭐ Reviews Bot (module)

Google Business (Maps) pe aane wale **customer reviews** ka **auto polite reply**.
Naya review aaye → AI ek achha, insaan-jaisा jawab likhe → Google pe post ho jaye.
Owner ka time bachta hai, har review ka jawab milta hai (ratings + trust badhta hai).

## Kaam kaise karta hai
```
Google Business review  ──▶  Reviews Worker (roz chalta hai)
                                   │  1) naye reviews laao (Google API)
                                   │  2) AI se reply banao (Gemini)  ← ai_reply.py
                                   │  3) reply Google pe post karo
                                   ▼
                          reviews_log (Supabase) me record
```

## Files
| File | Kaam | Ready? |
|------|------|--------|
| `ai_reply.py`   | AI reply generator (bot ka dimaag) | ✅ ab test ho sakta |
| `test_reply.py` | local test — bina Google ke reply dekho | ✅ |
| `config.py`     | env config | ✅ |
| `google_business.py` | Google se reviews laana + reply post | ⏳ (API access ke baad) |
| `worker.py`     | sab jodta hai, access-gate ke saath | ⏳ |

## ⚠️ Google API access chahiye (R7 — tumhara homework)
Reviews **laane/post** karne ke liye **Google Business Profile API** ka access
maangna padta hai (business verified + ek approval form). Steps `README` ke
neeche R7 me. Tab tak `ai_reply.py` ka brain **abhi** ready + testable hai.

## Access control
Ye bot bhi Master Bot ke gate se guzarta hai — `worker/access_check.py`:
`has_access(user_id, "reviews")` true hone par hi kaam karega. Admin dashboard ke
**⭐ Reviews** menu se on/off hota hai.

## Env chahiye
```
GEMINI_API_KEY=...        # AI reply ke liye (youtube module me already hai)
GEMINI_MODEL=gemini-2.0-flash   # optional, default
SUPABASE_URL=...
SUPABASE_SERVICE_KEY=...  # worker ke liye
```
