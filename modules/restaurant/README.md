# 🍔 Restaurant Orders (module)

WhatsApp/Zomato ke commission ke bina — apna **digital menu + ordering**.
Customer QR/link se menu kholta hai → order deta hai → owner ko turant dikhta hai.
**Poora self-contained** — koi bahar ki service nahi, sirf Supabase.

## 2 pages
| Page | Kaun | Kya |
|------|------|-----|
| `web/index.html` | 👤 Owner (login) | settings + menu manage + **live orders board** |
| `web/order.html?r=<slug>` | 🌐 Customer (no login) | menu dekhe → cart → order place kare |

## Flow
```
Owner: menu banata hai + "Open" karta hai   →  public link/QR share
Customer: order.html?r=slug  →  items add  →  naam+phone  →  Place order
Order  →  orders table (Supabase)  →  Owner board pe turant (15s auto-refresh)
Owner: Accept ▶ Preparing ▶ Ready ▶ Done   (ya Cancel)
```

## Setup
1. `schema.sql` Supabase me Run karo (restaurant_settings, menu_items, orders)
2. Admin dashboard → user ko **🍔 Restaurant** ON karo
3. Owner: bot page kholo → Settings me naam + slug save → Menu add → Open
4. Customer link (`order.html?r=slug`) share karo — QR bana ke table pe lagao

## Access control
Owner page Master Bot gate se guzarta hai (approved + 'restaurant' allowed).
Public order page ko gate nahi (customer to login karta hi nahi) — wo `slug` se
restaurant dhoondhta hai. RLS: menu/settings public-read, order koi bhi daale,
padhe sirf owner (apne orders).

## Aage (optional, baad me)
- Naya order aane pe owner ko WhatsApp/sound alert
- UPI payment link
- Order status customer ko dikhana (live)
