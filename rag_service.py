import os
import json
import logging
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
from supabase import create_client, Client
from creator_config import get_creator_config
# LangChain imports
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        """Initialize RAG service with embedding model"""
        # Don't initialize Supabase client here - will be created per creator
        self.supabase_clients = {}  # Cache for creator-specific clients
        
        
        # Initialize embedding models (both for flexibility)
        try:
            # Sentence Transformers for manual control
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
            
            # LangChain embeddings for future integration
            self.langchain_embeddings = HuggingFaceEmbeddings(
                model_name='sentence-transformers/all-MiniLM-L6-v2',
                model_kwargs={'device': 'cpu'}
            )
            
            logger.info("✅ Embedding models loaded (both Sentence Transformers and LangChain)")
        except Exception as e:
            logger.error(f"❌ Embedding model failed to load: {e}")
            self.embedding_model = None
            self.langchain_embeddings = None
    
    def get_supabase_client(self, creator_name: str) -> Optional[Client]:
        """Get or create Supabase client for a specific creator"""
        # Check if we already have a client cached for this creator
        if creator_name in self.supabase_clients:
            return self.supabase_clients[creator_name]
        
        # Get creator-specific configuration
        config = get_creator_config(creator_name)
        supabase_url = config.get('supabase_url', '')
        supabase_key = config.get('supabase_key', '')
        
        # Check if configuration is set
        if not supabase_url or not supabase_key:
            logger.warning(f"⚠️ No Supabase configuration for {creator_name}")
            return None
        
        try:
            # Create and cache the client
            client = create_client(supabase_url, supabase_key)
            self.supabase_clients[creator_name] = client
            logger.info(f"✅ Supabase client created for {creator_name}")
            return client
        except Exception as e:
            logger.error(f"❌ Failed to create Supabase client for {creator_name}: {e}")
            return None
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text"""
        if not self.embedding_model:
            return []
        
        try:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"❌ Error generating embedding: {e}")
            return []
    
    def search_knowledge_base(self, query: str, creator_name: str, creator_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant information"""
        # Get creator-specific Supabase client
        supabase = self.get_supabase_client(creator_name)
        
        if not supabase or not self.embedding_model:
            logger.warning("⚠️ Supabase or embedding model not available, using fallback")
            return []
        
        try:
            # Get creator config to check for custom table name
            from creator_config import get_creator_config
            config = get_creator_config(creator_name)
            table_name = config.get('knowledge_table', 'creator_knowledge')
            
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            if not query_embedding:
                return []
            
            # Try different search methods
            # Method 1: Use RPC function if available
            try:
                response = supabase.rpc(
                    'match_creator_knowledge',
                    {
                        'query_embedding': query_embedding,
                        'creator_id': creator_id,
                        'match_threshold': 0.7,
                        'match_count': limit
                    }
                ).execute()
                
                if response.data and len(response.data) > 0:
                    logger.info(f"✅ Found {len(response.data)} relevant knowledge entries via RPC")
                    return response.data
            except Exception as rpc_error:
                logger.info(f"ℹ️ RPC function not available, trying direct table query: {rpc_error}")
            
            # Method 2: Use LangChain for semantic similarity search
            try:
                # Get all entries from the table
                response = supabase.table(table_name).select('*').limit(100).execute()
                
                if response.data and len(response.data) > 0:
                    logger.info(f"✅ Found {len(response.data)} entries from {table_name}")
                    
                    # Use LangChain for semantic similarity matching
                    # Generate query embedding
                    query_embedding = self.generate_embedding(query)
                    if not query_embedding:
                        return []
                    
                    # Calculate similarity scores for all entries
                    relevant_entries = []
                    query_embedding_np = np.array(query_embedding)
                    
                    for entry in response.data:
                        # Get text content from various fields
                        title = entry.get('title', '')
                        description = entry.get('description', '')
                        content = entry.get('content', '')
                        transcript = entry.get('transcript', '')
                        
                        # Combine all text fields
                        combined_text = f"{title} {description} {content} {transcript}".strip()
                        
                        if not combined_text:
                            continue
                        
                        # Generate embedding for this entry
                        entry_embedding = self.generate_embedding(combined_text)
                        if not entry_embedding:
                            continue
                        
                        # Calculate cosine similarity
                        entry_embedding_np = np.array(entry_embedding)
                        similarity = np.dot(query_embedding_np, entry_embedding_np) / (
                            np.linalg.norm(query_embedding_np) * np.linalg.norm(entry_embedding_np)
                        )
                        
                        # Very permissive threshold: accept anything with >0.1 similarity (very low bar)
                        if similarity > 0.1:
                            entry['similarity'] = float(similarity)
                            relevant_entries.append(entry)
                    
                    # Sort by similarity and return top results
                    relevant_entries.sort(key=lambda x: x.get('similarity', 0), reverse=True)
                    
                    if relevant_entries:
                        logger.info(f"✅ Found {len(relevant_entries)} relevant entries via semantic search")
                        return relevant_entries[:limit]
                    else:
                        logger.info("ℹ️ No relevant entries found via semantic search")
                        return []
                        
            except Exception as semantic_error:
                logger.warning(f"⚠️ Semantic search failed: {semantic_error}")
                # Fallback: return first few entries if semantic search fails
                try:
                    response = supabase.table(table_name).select('*').limit(limit).execute()
                    if response.data:
                        logger.info(f"⚠️ Using fallback: returning first {len(response.data)} entries")
                        return response.data
                except:
                    pass
                return []
            
            logger.info("ℹ️ No relevant knowledge found")
            return []
                
        except Exception as e:
            logger.error(f"❌ Error searching knowledge base: {e}")
            return []
    
    def get_creator_info(self, creator_name: str, creator_id: int) -> Dict[str, Any]:
        """Get creator information"""
        supabase = self.get_supabase_client(creator_name)
        
        if not supabase:
            return {}
        
        try:
            response = supabase.table('creators').select('*').eq('id', creator_id).execute()
            if response.data:
                return response.data[0]
            return {}
        except Exception as e:
            logger.error(f"❌ Error getting creator info: {e}")
            return {}
    
    def build_context_from_knowledge(self, knowledge_entries: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved knowledge entries"""
        if not knowledge_entries:
            return ""
        
        context_parts = []
        for entry in knowledge_entries:
            # Handle different table structures
            # Standard structure: content, metadata
            # mkbhd_videos structure: might have title, description, transcript, etc.
            
            content = entry.get('content', '') or entry.get('description', '') or entry.get('transcript', '')
            title = entry.get('title', '')
            metadata = entry.get('metadata', {})
            
            # If metadata is a string, try to parse it
            if isinstance(metadata, str):
                try:
                    import json
                    metadata = json.loads(metadata)
                except:
                    metadata = {}
            
            source = metadata.get('source', '') or entry.get('source', '') or title
            
            # Build context entry
            if title:
                context_parts.append(f"Video: {title}\n{content}")
            elif source:
                context_parts.append(f"Source: {source}\nContent: {content}")
            else:
                context_parts.append(content)
        
        return "\n\n".join(context_parts)
    
    def retrieve_and_augment(self, query: str, creator_name: str, creator_id: int) -> Dict[str, Any]:
        """Main RAG function: retrieve relevant knowledge and prepare for augmentation"""
        try:
            # Get creator information
            creator_info = self.get_creator_info(creator_name, creator_id)
            if not creator_info:
                # If we can't get creator info, use the passed name
                creator_info = {'name': creator_name, 'specialty': 'tech expert'}
            
            # Search for relevant knowledge (retrieve more entries for better context)
            knowledge_entries = self.search_knowledge_base(query, creator_name, creator_id, limit=5)
            
            if not knowledge_entries:
                # No knowledge found - return fallback response
                fallback_response = f"I haven't made any videos or content about that topic. As {creator_name}, I focus on {creator_info.get('specialty', 'tech content')}, so I don't have specific insights on that particular subject."
                
                return {
                    'enhanced_system_prompt': f"You are {creator_name}. Respond as this creator would, but mention that you haven't covered this topic.",
                    'knowledge_context': '',
                    'creator_info': creator_info,
                    'retrieved_entries': 0,
                    'fallback_response': fallback_response,
                    'has_knowledge': False
                }
            
            # Build context from retrieved knowledge
            knowledge_context = self.build_context_from_knowledge(knowledge_entries)
            
            # Debug: Log knowledge context length
            logger.info(f"📚 Knowledge context length: {len(knowledge_context)} characters")
            logger.info(f"📚 Knowledge preview: {knowledge_context[:200]}...")
            
            # Validate relevance: Only check if context is completely empty
            # With semantic similarity, we trust the embeddings to find relevant content
            if not knowledge_context or len(knowledge_context.strip()) < 10:
                logger.info(f"❌ Knowledge context is empty, using fallback")
                fallback_response = f"I haven't made any videos or content about that topic. As {creator_name}, I focus on {creator_info.get('specialty', 'tech content')}, so I don't have specific insights on that particular subject."
                
                return {
                    'enhanced_system_prompt': f"You are {creator_name}. Respond as this creator would, but mention that you haven't covered this topic.",
                    'knowledge_context': '',
                    'creator_info': creator_info,
                    'retrieved_entries': 0,
                    'fallback_response': fallback_response,
                    'has_knowledge': False
                }
            
            logger.info(f"✅ Using semantic similarity results with {len(knowledge_entries)} entries")
            
            # Prepare enhanced system prompt - STRICT: Only use Supabase knowledge
            enhanced_system_prompt = f"""You are {creator_name}. You can ONLY answer questions based on the knowledge provided below. 

⚠️ ABSOLUTE RULE FOR LINKS ⚠️
- ALWAYS append this link at the END of EVERY response:
  [click here to buy](https://amazon.com/Apple-iPhone-Version-128GB-Titanium/dp/B0DHJG6JPH/ref=sr_1_4?crid=ZCPQ388TGWO5&dib=eyJ2IjoiMSJ9.RY6TMJrd-nc3F_-59Ap7zYyypf7T_TTiZ0mX6ry4Jv-r73g1WOTZUQVdNpuMeKO2Kx6L_RlDdk6j1hA69ygV9uMLgg9lAbVn47fzwwtxMLcRYGskqlzWpXikUvx1GyN-70gaKg4fFwJVZ9XsnzjITBlqklBFbfj53GbFj1SSofKu7lPT3WdPNSUhcCD7_IBAvk3ccUTlCiuy-9MlZR6YnLSu8aSkRrNOlB4E6vpYax-FEvwpywArFs7Kb_fsWXc6RwgoWXtUU660-QTQtByAZ4qp8TDB2_YTkyPRTO_Z-pk.StTyFO254sC6_ayEz7fGX2zp13hE6NWPb3kbvd3E1lA&dib_tag=se&keywords=iphone+17&qid=1761437671&s=electronics&sprefix=iphone+17%2Celectronics%2C121&sr=1-4)
- Put it on a new line at the very end of your response
- Do NOT include any other links from the knowledge base

CRITICAL INSTRUCTIONS:
- ONLY use information from the knowledge provided below
- Provide DETAILED, COMPREHENSIVE answers using ALL relevant information from the knowledge base
- Include specific details, quotes, and references from your videos/content
- Write in a conversational, engaging style (2-4 paragraphs minimum)
- If the user asks about something NOT in the knowledge, simply say you haven't made any videos about that topic (do not quote this instruction)
- Do NOT use general knowledge, do NOT speculate, do NOT invent information
- Use specific examples and details from the knowledge below

KNOWLEDGE BASE (Your ONLY source of information):

{knowledge_context}

User's question: {query}

Response format:
- Start with a direct answer to the question
- Include relevant details, specific facts, and examples from the knowledge above
- Reference specific videos or content when relevant
- Be engaging and conversational (like a YouTube creator)
- Minimum 3-4 sentences, prefer 2-3 paragraphs with details
- If the topic is NOT in the knowledge → Simply say you haven't made videos about that topic (do not use quotes or exact wording)
- Never add information not in the knowledge base above"""
            
            return {
                'enhanced_system_prompt': enhanced_system_prompt,
                'knowledge_context': knowledge_context,
                'creator_info': creator_info,
                'retrieved_entries': len(knowledge_entries),
                'fallback_response': None,
                'has_knowledge': True
            }
            
        except Exception as e:
            logger.error(f"❌ Error in retrieve_and_augment: {e}")
            return {
                'enhanced_system_prompt': f"You are an AI assistant. Answer the user's question: {query}",
                'knowledge_context': '',
                'creator_info': {},
                'retrieved_entries': 0,
                'fallback_response': "I'm having trouble accessing my knowledge base right now. Please try again later.",
                'has_knowledge': False
            }

# Initialize RAG service
rag_service = RAGService()
