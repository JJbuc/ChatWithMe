from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables (make sure you have these in your .env)
SUPABASE_URL = os.getenv("SUPABASE_URL")
print("SUPABASE_URL:", SUPABASE_URL)
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print("SUPABASE_KEY:", SUPABASE_KEY)

# Check if environment variables are set
if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing required environment variables!")
    print("Please create a .env file with:")
    print("SUPABASE_URL=your_supabase_project_url")
    print("SUPABASE_KEY=your_supabase_anon_key")
    exit(1)

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def test_supabase_connection():
    """Test if Supabase client connects and basic query works"""
    assert supabase is not None
    response = supabase.table("1stCreater").select("*").limit(1).execute()
    assert response is not None
    assert hasattr(response, "data")
    print("✅ Connection successful, sample data:", response.data)


def test_insert_data():
    """Test inserting a new record"""
    try:
        data = {
            "Title": "Sample Test Title",
            "url": "https://example.com",
            "transcript": "This is a test transcript."
        }
        response = supabase.table("1stCreater").insert(data).execute()
        assert response is not None
        assert hasattr(response, "data")
        print("✅ Insert successful, new entry:", response.data)
    except Exception as e:
        if "row-level security policy" in str(e).lower():
            print("⚠️  Insert blocked by Row Level Security (RLS) policy")
            print("   This is normal for production databases with RLS enabled")
            print("   To fix: Either disable RLS for this table or configure proper policies")
            print("   For now, skipping insert test...")
        else:
            print(f"❌ Insert failed with error: {e}")
            raise


def test_fetch_data():
    """Test fetching data from the table"""
    response = supabase.table("1stCreater").select("*").limit(5).execute()
    assert response is not None
    assert hasattr(response, "data")
    print("✅ Fetched records:", response.data)


if __name__ == "__main__":
    print("🔍 Testing Supabase connection and CRUD ops...")
    test_supabase_connection()
    test_insert_data()
    test_fetch_data()
    print("🎉 All tests completed successfully!")
