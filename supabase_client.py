from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load these from environment variables for security
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if environment variables are set
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Missing required environment variables. Please set SUPABASE_URL and SUPABASE_KEY in your .env file.\n"
        "Create a .env file with:\n"
        "SUPABASE_URL=your_supabase_project_url\n"
        "SUPABASE_KEY=your_supabase_anon_key"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)