# 🤖 Master Bot

Ek platform, bahut saare modules. Admin control karta hai kaun sa user
kaunsa module use kar sakta hai. YouTube, WhatsApp, Reviews... sab
"module" ki tarah plug hote hain.

## Folder structure
```
master_bot/
├─ supabase/      → database schema (roles + access control)
├─ admin/         → admin dashboard (users list + module toggle)
├─ user/          → user dashboard (allowed modules dikhein, baaki 🔒)
└─ worker/        → background worker checks (allowed? expiry?)
```

## Roles
| Role  | Kaun       | Kya kare                                             |
|-------|------------|------------------------------------------------------|
| admin | owner (tum)| users approve/block, module ON/OFF, sab dekhe        |
| user  | customer   | sirf allowed modules use kare                        |

## Database (Supabase)
- `profiles` — har user ka `role` (user/admin) + `status` (pending/approved/blocked)
- `module_access` — `user_id` + `module` + `allowed` + `expiry`
- `is_admin()` — RLS helper
- auto-trigger — naya signup → profile auto-ban jaye (`pending`)

Modules apne khud ke tables use karte hain (jaise YouTube ka
`channels`, `jobs` etc.) — ye layer sirf **access** control karti hai.

## Roadmap (step by step)
- [x] **Step 1** — DB: roles + module_access + RLS   ← `supabase/schema.sql`
- [x] **Step 2** — auto-profile trigger (schema me hai, bas run karna)
- [x] **Step 3** — Admin dashboard (users list + toggle)  ← `admin/index.html`
- [x] **Step 4** — User dashboard (locked/unlocked modules)  ← `user/index.html`
- [x] **Step 5** — Worker access-check helper ready  ← `worker/access_check.py`
- [ ] **Step 6** — YouTube ko module #1 me merge karo  ← `MIGRATION.md` (baad me)
- [ ] **Step 7** — Aage naye module (WhatsApp, Reviews...) plug karo

**Decision:** sab ek hi `master_bot` repo me (youtube = pehla module). Merge
"baad me" karna — tab tak youtube apne repo me chalta rahe. Steps: `MIGRATION.md`.

**Rule:** ek step complete → test → phir agla.
```
```
