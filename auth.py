# auth.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Fail fast if credentials are missing
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

# Create the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("✅ Server running and connected to Supabase")
