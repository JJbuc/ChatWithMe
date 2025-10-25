# ChatWithMe
Database for each creator 
Video
ffmpeg  ---> 80% if there is 80% similarity then hata do 
---> BLIP model 
---> SAM OWL
---> Sentiment analysis 
---> metadata 
Transcript
Description


{
time: 1 - 1:03
sentiment: angry
product_placed : iPhone 17
metadata : 
caption: 
transcript : 
}


Creator database
LLM 
frontend 



Knowledge graph --> edges (profit)



Text chuks (embedding)


user (embedding)

for all text_chinks:
return most similar 


user --> I want an iPhone which is 6 inch and 2 years old. 
context --> base on chunks 

Based on questiona nd chunk answer the question


Disadvantage?
1. Semantic search ---> 


Knowledge graph --> Find relevant node and perform hops 
Maximize the profit 


User --> I want an iPhone which is 6 inch and 2 years old.
Trace the graph while also maximizing profit 


v1 --> Transript + description --- > LLM ---> Frontend (both UI)
v2 --> Knowledge graph
v3 --> Images 
v4 --> Audio
v4 --> ranking 

## Architecture

The application follows a classic full-stack architecture:

```plaintext
🧍 User
   ↓
🌐 Frontend (HTML + CSS + JS)
   ↓ (fetch → API calls)
🐍 Backend (Python, FastAPI / Flask)
   ↓
🗄️ Supabase (PostgreSQL, Auth, Storage)