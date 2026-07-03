# modules/

Har bot yahan ek folder banega. Ye sirf **kaam** karte hain — access control
(kaun use kar sakta hai) upar `worker/access_check.py` handle karta hai.

```
modules/
├─ restaurant/  ← ✅ BANA + fully working (digital menu + ordering, sirf Supabase)
├─ reviews/     ← ✅ BANA (Google reviews auto-reply). Brain tested. Google API access baaki (R7)
└─ youtube/     ← baad me youtube_bot yahan aayega — dekho MIGRATION.md
   (aage: whatsapp/  missedcall/ ...)
```

### restaurant/ (fully working, abhi test ho sakta)
- `web/index.html` — owner: settings + menu manager + live orders board
- `web/order.html?r=<slug>` — public customer page (no login)
- `schema.sql` — restaurant_settings / menu_items / orders + RLS

### reviews/ (kaam kar raha, Google access pending)
- `ai_reply.py` — AI reply brain (tested ✓)  ·  `test_reply.py` — local test
- `google_business.py` — Google fetch/reply client (activates after R7)
- `worker.py` — gated worker (access_check "reviews")
- `schema.sql` — Supabase tables  ·  `web/` — user page
- `GOOGLE_SETUP.md` — R7 steps to get Google API access

Naya module banane ka pattern MIGRATION.md ke end me likha hai.
