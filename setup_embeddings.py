#!/usr/bin/env python3
"""
Setup script to populate embeddings in Supabase
Run this after setting up your Supabase database
"""

import os
import sys
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client

# Add current directory to path to import rag_service
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag_service import rag_service

def setup_embeddings():
    """Populate embeddings for all knowledge entries"""
    print("🚀 Starting embedding setup...")
    
    if not rag_service.supabase:
        print("❌ Supabase not configured. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")
        return
    
    if not rag_service.embedding_model:
        print("❌ Embedding model not loaded.")
        return
    
    try:
        # Get all knowledge entries without embeddings
        response = rag_service.supabase.table('creator_knowledge').select('*').is_('embedding', 'null').execute()
        
        if not response.data:
            print("✅ All entries already have embeddings!")
            return
        
        print(f"📝 Found {len(response.data)} entries without embeddings")
        
        # Process each entry
        for entry in response.data:
            content = entry['content']
            entry_id = entry['id']
            
            print(f"🔄 Processing entry {entry_id}: {content[:50]}...")
            
            # Generate embedding
            embedding = rag_service.generate_embedding(content)
            
            if embedding:
                # Update the entry with embedding
                update_response = rag_service.supabase.table('creator_knowledge').update({
                    'embedding': embedding
                }).eq('id', entry_id).execute()
                
                if update_response.data:
                    print(f"✅ Updated entry {entry_id}")
                else:
                    print(f"❌ Failed to update entry {entry_id}")
            else:
                print(f"❌ Failed to generate embedding for entry {entry_id}")
        
        print("🎉 Embedding setup complete!")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")

if __name__ == "__main__":
    setup_embeddings()
