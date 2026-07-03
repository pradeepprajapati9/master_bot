# R7 — Google Business Profile API access (Reviews bot ko "live" karna)

Reviews **laane + reply post** karne ke liye Google se ek special API ka access
chahiye. Ye ek baar ka setup hai. Steps neeche — dhyaan se karo.

> Tab tak bot ka **brain (AI reply) ready + tested** hai. Ye access aate hi
> bot asli reviews pe kaam karne lagega — koi code change nahi.

## Pehle ye hona chahiye
- [ ] Ek **Google Business Profile** (Google Maps pe tumhara business listed +
      **verified**). Agar nahi hai: business.google.com pe bana + verify karo.

## Step 1 — Google Cloud project (youtube wala reuse kar sakte ho)
1. console.cloud.google.com kholo
2. Wahi project chuno jo youtube_bot use karta hai (ya naya banao)

## Step 2 — API access maango (ye approval wala part hai)
Google Business Profile ke reviews API **restricted** hain — access form bharna padta hai:
1. Kholo: **Google Business Profile APIs** access request form
   (search: "Google Business Profile API access request form" → official Google form)
2. Form me: project number, business details, use-case ("apne business ke
   reviews ka management/auto-reply") bharo → submit
3. Google review karega — **kuch din (kabhi 1-2 hafte) lag sakte hain**
4. Approve hone pe email aayega

## Step 3 — APIs enable karo (project me)
Approval ke baad, Cloud Console → "APIs & Services" → Enable:
- [ ] **My Business Account Management API**
- [ ] **My Business Business Information API**
- [ ] **Google My Business API** (v4 — reviews/reply yahin se)

## Step 4 — OAuth consent + scope
1. "APIs & Services" → OAuth consent screen
2. Scope add karo: `https://www.googleapis.com/auth/business.manage`
3. Test users me apna + clients ke Gmail add karo (jab tak app "testing" me hai)

## Step 5 — Creds worker ko do (GitHub Secrets)
master_bot repo → Settings → Secrets and variables → Actions → New secret:
- `GOOGLE_CLIENT_ID`      (OAuth client)
- `GOOGLE_CLIENT_SECRET`
- `GEMINI_API_KEY`        (AI reply — youtube wali same)
- `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`

## Step 6 — Account/Location id
Bot ko `account_id` + `location_id` chahiye (kis business ke reviews).
Ye connect-flow (user page ka "Connect Google Business") set karega —
wo OAuth R7 approval ke baad activate hoga. (`google_business.py` ready hai.)

---

### Ho gaya to
`reviews_connections.connected = true` + token save → worker har schedule pe
naye reviews laayega, AI reply banayega, post karega, `reviews_log` me likhega.
User apne dashboard pe history dekhega.
