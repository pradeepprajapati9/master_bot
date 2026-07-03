# 🔀 YouTube ko Master Bot me laane ka plan (baad me karna)

**Decision:** sab ek hi `master_bot` repo me — youtube ek module banega.
Ye disruptive hai (youtube abhi live hai), isliye ye guide **tab** follow karo
jab poora time ho. Tab tak youtube apne repo me chalta rahega — koi problem nahi.

## Target structure
```
master_bot/                 ← single git repo
├─ admin/index.html         ✅ (ban gaya)
├─ user/index.html          ✅ (ban gaya)
├─ supabase/schema.sql      ✅ (ban gaya)
├─ worker/access_check.py   ✅ (shared gate — sab modules use karenge)
└─ modules/
   └─ youtube/              ← youtube_bot yahan aayega
      ├─ bot/  worker.py  enqueue_daily.py  config.py ...
      └─ web/dashboard.html
```

## Steps (jab merge karna ho)
1. **Copy** `youtube_bot/` ka poora content → `master_bot/modules/youtube/`
   (venv/, output/, credentials/, .git/ chhod dena — sirf code).
2. **Worker gate lagao** — `modules/youtube/worker.py` aur `enqueue_daily.py` me:
   ```python
   import sys, os
   sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
   from worker.access_check import has_access, allowed_user_ids

   # enqueue_daily.py me — sirf allowed users ko daily job do:
   ok = allowed_user_ids("youtube")
   ...
   if uid not in ok:
       continue

   # worker.py me — build se pehle:
   if not has_access(job["user_id"], "youtube"):
       sb_patch("jobs", {"status":"error","error":"access not allowed"}, id=f"eq.{job['id']}")
       continue
   ```
3. **GitHub Actions** — youtube ke `worker.yml` + `pages.yml` ko master_bot repo me
   le aao. Paths update karo (`modules/youtube/...`). Pages ab
   `master_bot/user/` (ya admin/) serve kare.
4. **Secrets** dobara add karo master_bot repo ke Settings → Secrets me
   (SUPABASE_URL, SUPABASE_SERVICE_KEY, GOOGLE_CLIENT_ID/SECRET, GEMINI, PEXELS).
5. **Test** ek run → youtube waise hi kaam kare, bas ab access-gate ke saath.
6. Purana `youtube_bot` repo archive kar do.

## Naya module add karne ka pattern (future)
1. `modules/<naam>/` me code daalo.
2. `worker/access_check.py` se `has_access(uid, "<naam>")` gate lagao.
3. `admin/index.html` + `user/index.html` ke `MODULES` list me ek line add karo.
4. Bas — admin toggle karega, user ko dikhega, worker check karega.
