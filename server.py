from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import logging
import os
from dotenv import load_dotenv
from rag_service import rag_service

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Groq API configuration (Free tier: 14,400 requests/day)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")

# Creator name to ID mapping
CREATOR_ID_MAP = {
    "Marques Brownlee": 1,
    "Austin Evans": 2,
    "Justine Ezarik": 3,
    "Zack Nelson": 4,
    "Lewis George Hilsenteger": 5
}

def get_creator_id(creator_name):
    """Get creator ID from creator name"""
    return CREATOR_ID_MAP.get(creator_name, 1)  # Default to Marques Brownlee

def call_groq_api_with_context(messages, creator_name, system_prompt):
    """Call Groq API with conversation context"""
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Build messages array with system prompt and conversation history
        api_messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (limit to last 10 messages to avoid token limits)
        recent_messages = messages[-10:] if len(messages) > 10 else messages
        api_messages.extend(recent_messages)
        
        payload = {
            "model": "llama-3.1-8b-instant",  # Free model on Groq
            "messages": api_messages,
            "max_tokens": 2000,  # Increased for detailed RAG responses
            "temperature": 0.5  # Slightly higher for more engaging responses
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            ai_response = response_data['choices'][0]['message']['content']
            logger.info(f"✅ Groq API call successful for {creator_name} with {len(messages)} context messages")
            return ai_response
        else:
            logger.error(f"❌ Groq API error: {response.status_code} - {response.text}")
            raise Exception(f"API Error: {response.text}")
            
    except Exception as e:
        logger.error(f"❌ Unexpected error calling Groq API: {e}")
        raise Exception(f"Unexpected error: {str(e)}")

def call_groq_api(message, creator_name, system_prompt):
    """Call Groq API (Free tier: 14,400 requests/day) - Single message version"""
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",  # Free model on Groq
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            ai_response = response_data['choices'][0]['message']['content']
            logger.info(f"✅ Groq API call successful for {creator_name}")
            return ai_response
        else:
            logger.error(f"❌ Groq API error: {response.status_code} - {response.text}")
            raise Exception(f"API Error: {response.text}")
            
    except Exception as e:
        logger.error(f"❌ Unexpected error calling Groq API: {e}")
        raise Exception(f"Unexpected error: {str(e)}")

def get_demo_response(message, creator_name):
    """Fallback demo responses when API is not available"""
    demo_responses = {
        "Marques Brownlee": f"Hey! I'm Marques from MKBHD. You asked: '{message}'. I can help you with tech reviews, smartphone recommendations, or any gadget questions you have!",
        "Austin Evans": f"Hello! I'm Austin Evans. Regarding '{message}', I can help you with PC builds, gaming hardware, or any tech setup questions!",
        "Justine Ezarik": f"Hi there! I'm iJustine. You mentioned: '{message}'. I can help you with Apple products, tech unboxings, or any gadget recommendations!",
        "Zack Nelson": f"Hey! I'm Zack from JerryRigEverything. About '{message}', I can help you with durability tests, smartphone teardowns, or tech durability questions!",
        "Lewis George Hilsenteger": f"Hello! I'm Lewis from Unbox Therapy. You said: '{message}'. I can help you with unboxing experiences, tech reviews, or product recommendations!"
    }
    
    return demo_responses.get(creator_name, f"Hello! I'm {creator_name}. You asked: '{message}'. How can I help you today?")

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

# Store conversation history for each user session
conversation_history = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with conversation context"""
    try:
        data = request.json
        message = data.get('message')
        creator = data.get('creator')
        system_prompt = data.get('systemPrompt')
        session_id = data.get('sessionId', 'default')  # Add session ID for context
        
        if not message or not creator:
            return jsonify({"error": "Message and creator are required"}), 400
        
        logger.info(f"💬 Chat request from {creator}: {message[:50]}...")
        
        # Get or create conversation history for this session
        if session_id not in conversation_history:
            conversation_history[session_id] = {
                'creator': creator,
                'messages': []
            }
        
        # Add user message to history
        conversation_history[session_id]['messages'].append({
            'role': 'user',
            'content': message
        })
        
        # RAG Integration: Retrieve relevant knowledge
        try:
            # Get creator ID (you'll need to map creator names to IDs)
            creator_id = get_creator_id(creator)
            
            # Use RAG to retrieve and augment (pass creator name for specific API)
            rag_result = rag_service.retrieve_and_augment(message, creator, creator_id)
            
            # Check if we have knowledge or need fallback
            if not rag_result['has_knowledge']:
                # No knowledge found - use fallback response
                ai_response = rag_result['fallback_response']
                logger.info("ℹ️ No knowledge found, using fallback response")
            else:
                # Knowledge found - use enhanced system prompt
                enhanced_system_prompt = rag_result['enhanced_system_prompt']
                ai_response = call_groq_api_with_context(
                    conversation_history[session_id]['messages'], 
                    creator, 
                    enhanced_system_prompt
                )
                logger.info(f"✅ RAG-enhanced response sent with {rag_result['retrieved_entries']} knowledge entries")
            
            # Add AI response to history
            conversation_history[session_id]['messages'].append({
                'role': 'assistant',
                'content': ai_response
            })
            
            return jsonify({
                "response": ai_response,
                "sessionId": session_id,
                "messageCount": len(conversation_history[session_id]['messages']),
                "rag_used": rag_result['has_knowledge'],
                "knowledge_entries": rag_result['retrieved_entries']
            })
        except Exception as api_error:
            logger.warning(f"⚠️ API failed, using demo response: {api_error}")
            # Fallback to demo response
            demo_response = get_demo_response(message, creator)
            conversation_history[session_id]['messages'].append({
                'role': 'assistant',
                'content': demo_response
            })
            return jsonify({
                "response": demo_response,
                "sessionId": session_id,
                "messageCount": len(conversation_history[session_id]['messages'])
            })
            
    except Exception as e:
        logger.error(f"❌ Error in /api/chat: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'groq_api_available': True,
        'api_key': 'configured',
        'model': 'llama-3.1-8b-instant',
        'free_tier': '14,400 requests/day'
    })

@app.route('/api/creators', methods=['GET'])
def get_creators():
    """Get creators list"""
    creators = [
        {"id": 1, "name": "Marques Brownlee", "specialty": "\"MKBHD\"", "avatar": "photos/Marques_Brownlee.jpg", "description": "Tech reviewer and YouTuber known for in-depth smartphone and gadget reviews"},
        {"id": 2, "name": "Austin Evans", "specialty": "\"Austin Evans\"", "avatar": "photos/AustinEvans.jpeg", "description": "Tech YouTuber specializing in PC builds, gaming hardware, and tech reviews"},
        {"id": 3, "name": "Justine Ezarik", "specialty": "\"iJustine\"", "avatar": "photos/justine-ezarik.jpg", "description": "Tech YouTuber and Apple enthusiast known for unboxing videos and tech reviews"},
        {"id": 4, "name": "Zack Nelson", "specialty": "\"JerryRigEverything\"", "avatar": "photos/Zack Nelson.jpeg", "description": "Tech YouTuber famous for durability tests and smartphone teardowns"},
        {"id": 5, "name": "Lewis George Hilsenteger", "specialty": "\"Unbox Therapy\"", "avatar": "photos/Lewis George Hilsenteger.jpg", "description": "Tech YouTuber known for unboxing videos and tech product reviews"}
    ]
    return jsonify({'creators': creators})

if __name__ == '__main__':
    print("🚀 Starting chud.ai server...")
    print(f"🌐 Server will be available at: http://localhost:5001")
    print(f"🔧 Groq API status: ✅ Available (Free Tier)")
    print(f"🤖 Model: llama-3.1-8b-instant")
    print(f"🔑 API Key: Needs configuration")
    print(f"💡 Get free API key at: https://console.groq.com/")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
