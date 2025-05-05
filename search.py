from sentence_transformers import SentenceTransformer
import numpy as np
import sqlite3

model = SentenceTransformer('all-MiniLM-L6-v2')

def search_clips(query, top_k=5):
    # Get all clips from DB
    conn = sqlite3.connect("clipboard.db")
    c = conn.cursor()
    c.execute("SELECT id, content FROM clips WHERE content_type='text'")
    clips = c.fetchall()
    
    # Encode query and clips
    query_embedding = model.encode(query)
    clip_embeddings = model.encode([clip[1] for clip in clips])
    
    # Calculate similarities
    similarities = np.dot(clip_embeddings, query_embedding)
    
    # Get top matches
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [clips[i] for i in top_indices]