-- ============================================================
-- MASTER BOT — Step 1: Roles + Access control
-- Paste this whole file into: Supabase -> SQL Editor -> New query -> Run
-- (Safe to re-run — sab "if not exists" hai.)
-- ============================================================

-- ------------------------------------------------------------
-- 1) PROFILES — har user ka role + approval status
--    role:   'user'  | 'admin'
--    status: 'pending' | 'approved' | 'blocked'
-- ------------------------------------------------------------
create table if not exists public.profiles (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  email      text,
  role       text default 'user',
  status     text default 'pending',
  created_at timestamptz default now()
);

-- ------------------------------------------------------------
-- 2) MODULE_ACCESS — kis user ke paas kaunsa module allowed hai
--    module: 'youtube' | 'whatsapp' | 'reviews' | ...
--    allowed: true/false   |   expiry: kab tak (null = no limit)
-- ------------------------------------------------------------
create table if not exists public.module_access (
  user_id  uuid not null references auth.users(id) on delete cascade,
  module   text not null,
  allowed  boolean default false,
  expiry   date,
  updated_at timestamptz default now(),
  primary key (user_id, module)
);

-- ------------------------------------------------------------
-- 3) Helper: "kya ye current user admin hai?"
--    (RLS policies isko use karti hain)
-- ------------------------------------------------------------
create or replace function public.is_admin()
returns boolean
language sql
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.profiles
    where user_id = auth.uid() and role = 'admin'
  );
$$;

-- ------------------------------------------------------------
-- 4) Row Level Security
-- ------------------------------------------------------------
alter table public.profiles      enable row level security;
alter table public.module_access enable row level security;

-- PROFILES:
--  - user apni hi profile padh sake
--  - admin sabki profile padh + edit kar sake
drop policy if exists "read own profile"   on public.profiles;
drop policy if exists "admin read all"     on public.profiles;
drop policy if exists "admin write all"    on public.profiles;

create policy "read own profile" on public.profiles
  for select using (auth.uid() = user_id);

create policy "admin read all" on public.profiles
  for select using (public.is_admin());

create policy "admin write all" on public.profiles
  for all using (public.is_admin()) with check (public.is_admin());

-- MODULE_ACCESS:
--  - user apni hi access-list padh sake (dashboard me lock/unlock dikhane ko)
--  - admin sab padh + toggle kar sake
drop policy if exists "read own access"  on public.module_access;
drop policy if exists "admin manage all" on public.module_access;

create policy "read own access" on public.module_access
  for select using (auth.uid() = user_id);

create policy "admin manage all" on public.module_access
  for all using (public.is_admin()) with check (public.is_admin());

-- ------------------------------------------------------------
-- 5) AUTO-PROFILE: jab bhi naya user signup kare,
--    uski profile apne aap ban jaye (status = 'pending')
-- ------------------------------------------------------------
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (user_id, email, role, status)
  values (new.id, new.email, 'user', 'pending')
  on conflict (user_id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ============================================================
-- 6) TUMHE ADMIN banane ke liye (ek baar chalao):
--    Neeche apna email daalo. Pehle ek baar dashboard pe
--    login kar lena taaki auth.users me tumhari entry ban jaye.
-- ============================================================
-- update public.profiles
--   set role = 'admin', status = 'approved'
--   where email = 'TUMHARA_EMAIL@gmail.com';
