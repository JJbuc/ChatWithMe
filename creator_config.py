"""
Configuration for creator-specific Supabase APIs
Each creator has their own Supabase project and API keys
"""

# Creator-specific Supabase configurations
CREATOR_SUPABASE_CONFIG = {
    "Marques Brownlee": {
        "supabase_url": "https://xqswazwghqvofdkjalxx.supabase.co",
        "supabase_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhxc3dhendnaHF2b2Zka2phbHh4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzNjk4MDksImV4cCI6MjA3Njk0NTgwOX0.os_aVagXj9WCbbQ0TvVZ2EaPtF0s_THj_Vj-G3izd_k",
        "knowledge_table": "mkbhd_videos",  # Custom table name for MKBHD
    },
    "Austin Evans": {
        "supabase_url": "",
        "supabase_key": "",
    },
    "Justine Ezarik": {
        "supabase_url": "https://erojldajyliybqtnvops.supabase.co",
        "supabase_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVyb2psZGFqeWxpeWJxdG52b3BzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE0MTY4NTUsImV4cCI6MjA3Njk5Mjg1NX0.UWNncCN9EdSX-Qnes89CURPE5EnL0viVwXR7vvD1kJc",
        "knowledge_table": "justine_videos",  # Custom table name for iJustine
    },
    "Zack Nelson": {
        "supabase_url": "",
        "supabase_key": "",
    },
    "Lewis George Hilsenteger": {
        "supabase_url": "",
        "supabase_key": "",
    }
}

def get_creator_config(creator_name: str) -> dict:
    """Get Supabase configuration for a specific creator"""
    return CREATOR_SUPABASE_CONFIG.get(creator_name, {
        "supabase_url": "",
        "supabase_key": ""
    })

def set_creator_config(creator_name: str, url: str, key: str):
    """Set Supabase configuration for a specific creator"""
    if creator_name in CREATOR_SUPABASE_CONFIG:
        CREATOR_SUPABASE_CONFIG[creator_name]["supabase_url"] = url
        CREATOR_SUPABASE_CONFIG[creator_name]["supabase_key"] = key
        print(f"✅ Updated {creator_name} Supabase configuration")
    else:
        print(f"❌ Creator '{creator_name}' not found")
