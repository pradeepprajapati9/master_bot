-- ============================================================
-- RESTAURANT MODULE — Supabase tables
-- Paste into: Supabase -> SQL Editor -> New query -> Run
-- (Master Bot ke schema.sql ke BAAD chalao)
--
-- NOTE: is bot me customer LOGIN nahi karta (public order page).
-- Isliye menu + settings PUBLIC readable hain, aur order koi bhi daal sakta hai.
-- Order ko PADH sirf owner sakta hai (apne hi orders).
-- ============================================================

-- 1) Restaurant ki settings (public url ke liye slug bhi)
create table if not exists public.restaurant_settings (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  name       text,
  slug       text unique,                 -- public order link: order.html?r=<slug>
  phone      text,
  currency   text default '₹',
  is_open    boolean default true,
  updated_at timestamptz default now()
);

-- 2) Menu items
create table if not exists public.menu_items (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) on delete cascade,
  name        text not null,
  description text,
  price       numeric not null default 0,
  category    text,
  available   boolean default true,
  sort        int default 0,
  created_at  timestamptz default now()
);

-- 3) Orders (customer daale, owner dekhe/manage kare)
create table if not exists public.orders (
  id             uuid primary key default gen_random_uuid(),
  user_id        uuid not null references auth.users(id) on delete cascade,
  customer_name  text,
  customer_phone text,
  table_no       text,
  items          jsonb,                    -- [{name, price, qty}]
  total          numeric,
  note           text,
  status         text default 'new',       -- new | preparing | ready | done | cancelled
  created_at     timestamptz default now()
);

-- ============================================================
-- RLS
-- ============================================================
alter table public.restaurant_settings enable row level security;
alter table public.menu_items          enable row level security;
alter table public.orders              enable row level security;

-- settings: sab padh sakein (public order page ko chahiye), owner hi likhe
drop policy if exists "public read settings" on public.restaurant_settings;
drop policy if exists "own settings"         on public.restaurant_settings;
create policy "public read settings" on public.restaurant_settings for select using (true);
create policy "own settings" on public.restaurant_settings
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- menu: available items sab dekhein, owner apne sab manage kare
drop policy if exists "public read menu" on public.menu_items;
drop policy if exists "own menu"         on public.menu_items;
create policy "public read menu" on public.menu_items for select using (available = true);
create policy "own menu" on public.menu_items
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- orders: koi bhi order DAAL sake (public), padhe/manage sirf owner
drop policy if exists "public place order" on public.orders;
drop policy if exists "own orders"         on public.orders;
create policy "public place order" on public.orders for insert with check (true);
create policy "own orders" on public.orders
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
