-- ============================================================
-- REVIEWS MODULE — Supabase tables
-- Paste into: Supabase -> SQL Editor -> New query -> Run
-- (Master Bot ke schema.sql ke BAAD chalao — auth.users pe depend karta hai)
-- ============================================================

-- 1) User ne apna Google Business connect kiya (non-secret info)
create table if not exists public.reviews_connections (
  user_id      uuid primary key references auth.users(id) on delete cascade,
  account_name text,          -- Google account/location ka naam
  location_id  text,          -- kis location ke reviews
  connected    boolean default false,
  updated_at   timestamptz default now()
);

-- 2) Google OAuth refresh token (SECRET). RLS on, koi client policy nahi ->
--    browser kabhi nahi padh sakta. Sirf worker (service_role) padhta hai.
create table if not exists public.reviews_tokens (
  user_id       uuid primary key references auth.users(id) on delete cascade,
  refresh_token text not null,
  updated_at    timestamptz default now()
);

-- 3) User ki reply settings
create table if not exists public.reviews_settings (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  business   text,                         -- business ka naam (reply me use hota)
  tone       text default 'friendly',      -- friendly | professional | short
  language   text default 'English',
  signature  text default '',              -- reply ke end me (optional)
  auto_reply boolean default true,
  updated_at timestamptz default now()
);

-- 4) Kaun-kaun se reviews ka reply diya (dobara reply na ho + history)
create table if not exists public.reviews_log (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) on delete cascade,
  review_id   text not null,               -- Google review id
  rating      int,
  review_text text,
  reply_text  text,
  status      text default 'replied',      -- replied | skipped | error
  created_at  timestamptz default now(),
  unique (user_id, review_id)              -- ek review ka ek hi reply
);

-- ============================================================
-- RLS: har user sirf apna data dekhe
-- ============================================================
alter table public.reviews_connections enable row level security;
alter table public.reviews_tokens      enable row level security;  -- no policy = client-locked
alter table public.reviews_settings    enable row level security;
alter table public.reviews_log         enable row level security;

drop policy if exists "own conn" on public.reviews_connections;
create policy "own conn" on public.reviews_connections
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own settings" on public.reviews_settings;
create policy "own settings" on public.reviews_settings
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "own log read" on public.reviews_log;
create policy "own log read" on public.reviews_log
  for select using (auth.uid() = user_id);

-- reviews_tokens: user apna token save/update kar sake, par padh NA sake
drop policy if exists "save own rtoken"   on public.reviews_tokens;
drop policy if exists "update own rtoken" on public.reviews_tokens;
create policy "save own rtoken"   on public.reviews_tokens for insert with check (auth.uid() = user_id);
create policy "update own rtoken" on public.reviews_tokens for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
