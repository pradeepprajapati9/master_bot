# modules/

Har bot yahan ek folder banega. Ye sirf **kaam** karte hain — access control
(kaun use kar sakta hai) upar `worker/access_check.py` handle karta hai.

```
modules/
├─ reviews/     ← ✅ BANA (Google reviews auto-reply). Brain tested. Google API access baaki (R7)
└─ youtube/     ← baad me youtube_bot yahan aayega — dekho MIGRATION.md
   (aage: whatsapp/  missedcall/  restaurant/ ...)
```

### reviews/ (kaam kar raha, Google access pending)
- `ai_reply.py` — AI reply brain (tested ✓)  ·  `test_reply.py` — local test
- `google_business.py` — Google fetch/reply client (activates after R7)
- `worker.py` — gated worker (access_check "reviews")
- `schema.sql` — Supabase tables  ·  `web/` — user page
- `GOOGLE_SETUP.md` — R7 steps to get Google API access

Naya module banane ka pattern MIGRATION.md ke end me likha hai.
