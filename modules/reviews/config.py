"""Reviews module — config (env se padhta hai)."""
import os

# AI (reply generate karne ke liye) — youtube module me ye key already hai
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Supabase (worker ke liye — service key RLS bypass karta hai)
SUPABASE_URL        = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

# is module ka naam (access_check gate isi naam se check karta hai)
MODULE = "reviews"
