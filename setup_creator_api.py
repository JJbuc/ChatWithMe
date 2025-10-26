#!/usr/bin/env python3
"""
Setup script to configure creator-specific Supabase APIs
"""

from creator_config import set_creator_config

def setup_mkbhd_api():
    """Set up MKBHD Supabase API"""
    print("🔧 Setting up MKBHD Supabase API")
    print("Please provide your MKBHD Supabase credentials:")
    
    url = input("Enter MKBHD Supabase URL: ").strip()
    key = input("Enter MKBHD Supabase Key: ").strip()
    
    if url and key:
        set_creator_config("Marques Brownlee", url, key)
        print("\n✅ MKBHD API configured successfully!")
    else:
        print("❌ Invalid credentials provided")
    
    return url, key

def setup_all_creators():
    """Set up all creator APIs"""
    creators = [
        "Marques Brownlee",
        "Austin Evans",
        "Justine Ezarik",
        "Zack Nelson",
        "Lewis George Hilsenteger"
    ]
    
    print("🔧 Setting up Creator APIs")
    
    for creator in creators:
        print(f"\n--- {creator} ---")
        url = input("Supabase URL (or press Enter to skip): ").strip()
        key = input("Supabase Key (or press Enter to skip): ").strip()
        
        if url and key:
            set_creator_config(creator, url, key)
    
    print("\n✅ Creator APIs configured!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        setup_all_creators()
    else:
        setup_mkbhd_api()
