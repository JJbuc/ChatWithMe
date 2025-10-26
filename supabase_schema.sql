-- Enable vector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Creators table
CREATE TABLE IF NOT EXISTS creators (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    expertise_areas TEXT[],
    knowledge_summary TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Creator knowledge base with embeddings
CREATE TABLE IF NOT EXISTS creator_knowledge (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES creators(id),
    content TEXT NOT NULL,
    embedding VECTOR(384), -- For all-MiniLM-L6-v2 model
    metadata JSONB,
    source TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Function for vector similarity search
CREATE OR REPLACE FUNCTION match_creator_knowledge(
    query_embedding VECTOR(384),
    creator_id INTEGER,
    match_threshold FLOAT DEFAULT 0.7,
    match_count INTEGER DEFAULT 5
)
RETURNS TABLE (
    id INTEGER,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE SQL
AS $$
    SELECT 
        creator_knowledge.id,
        creator_knowledge.content,
        creator_knowledge.metadata,
        1 - (creator_knowledge.embedding <=> query_embedding) AS similarity
    FROM creator_knowledge
    WHERE creator_knowledge.creator_id = $2
    AND 1 - (creator_knowledge.embedding <=> query_embedding) > $3
    ORDER BY creator_knowledge.embedding <=> query_embedding
    LIMIT $4;
$$;

-- Insert sample creators
INSERT INTO creators (id, name, specialty, expertise_areas, knowledge_summary) VALUES
(1, 'Marques Brownlee', 'Tech Reviewer', ARRAY['Smartphones', 'Cameras', 'Tech Reviews'], 'Expert in smartphone reviews, camera technology, and consumer electronics'),
(2, 'Austin Evans', 'PC Builder', ARRAY['PC Building', 'Gaming Hardware', 'Tech Reviews'], 'Specializes in PC builds, gaming hardware, and tech reviews'),
(3, 'Justine Ezarik', 'Apple Enthusiast', ARRAY['Apple Products', 'Lifestyle Tech', 'App Reviews'], 'Apple ecosystem expert and lifestyle tech reviewer'),
(4, 'Zack Nelson', 'Durability Tester', ARRAY['Durability Tests', 'Teardowns', 'Build Quality'], 'Famous for smartphone durability tests and teardowns'),
(5, 'Lewis George Hilsenteger', 'Unboxing Expert', ARRAY['Unboxing', 'Product Reviews', 'First Impressions'], 'Known for unboxing videos and first impressions of tech products')
ON CONFLICT (id) DO NOTHING;

-- Sample knowledge entries (you'll replace these with real data)
INSERT INTO creator_knowledge (creator_id, content, metadata, source) VALUES
(1, 'The iPhone 15 Pro has a 48MP main camera with improved low-light performance and better computational photography.', '{"topic": "iPhone 15 Pro", "category": "Camera"}', 'iPhone 15 Pro Review'),
(1, 'Samsung Galaxy S24 Ultra features a 200MP camera sensor with excellent zoom capabilities up to 10x optical zoom.', '{"topic": "Samsung Galaxy S24", "category": "Camera"}', 'Galaxy S24 Ultra Review'),
(2, 'For gaming, I recommend RTX 4070 or RTX 4080 graphics cards for 1440p gaming at high settings.', '{"topic": "Gaming Graphics Cards", "category": "PC Building"}', 'Gaming PC Build Guide'),
(2, 'AMD Ryzen 7 7800X3D is currently the best gaming CPU with excellent performance per dollar.', '{"topic": "Gaming CPU", "category": "PC Building"}', 'Best Gaming CPU 2024'),
(3, 'The Apple Watch Series 9 has improved health tracking features and faster S9 chip performance.', '{"topic": "Apple Watch Series 9", "category": "Apple Products"}', 'Apple Watch Series 9 Review'),
(4, 'iPhone 15 Pro passed the bend test but showed some flex in the titanium frame under extreme pressure.', '{"topic": "iPhone 15 Pro", "category": "Durability Test"}', 'iPhone 15 Pro Bend Test'),
(5, 'The new MacBook Pro M3 has incredible battery life lasting over 18 hours of normal use.', '{"topic": "MacBook Pro M3", "category": "Apple Products"}', 'MacBook Pro M3 Unboxing')
ON CONFLICT DO NOTHING;

-- Generate embeddings for existing content (you'll need to run this after setting up the embedding service)
-- UPDATE creator_knowledge SET embedding = generate_embedding(content) WHERE embedding IS NULL;
