import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
from models import Document, DocumentChunk, get_db

class SimpleVectorStore:
    def __init__(self):
        # Using a lightweight model for demonstration
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for a list of texts"""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into chunks with overlap"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            if chunk_words:
                chunk = " ".join(chunk_words)
                chunks.append(chunk)
        
        return chunks
    
    def store_chunks(self, document_id: int, chunks: List[str], db):
        """Store chunks with embeddings in database"""
        embeddings = self.create_embeddings(chunks)
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            db_chunk = DocumentChunk(
                document_id=document_id,
                chunk_text=chunk,
                chunk_index=i,
                embedding=json.dumps(embedding)
            )
            db.add(db_chunk)
        
        db.commit()
    
    def search_similar(self, query: str, note_id: int = None, top_k: int = 3, db=None) -> List[Tuple[DocumentChunk, float]]:
        """Search for similar chunks"""
        # Create query embedding
        query_embedding = self.model.encode([query])[0]
        
        # Get all chunks
        if note_id:
            # Use subquery to filter by note_id
            chunks = db.query(DocumentChunk).filter(
                DocumentChunk.document_id.in_(
                    db.query(Document.id).filter(Document.note_id == note_id)
                )
            ).all()
        else:
            chunks = db.query(DocumentChunk).all()
        
        if not chunks:
            return []
        
        # Calculate similarities
        similarities = []
        for chunk in chunks:
            chunk_embedding = np.array(json.loads(chunk.embedding))
            similarity = cosine_similarity([query_embedding], [chunk_embedding])[0][0]
            similarities.append((chunk, similarity))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

# Global vector store instance
vector_store = SimpleVectorStore()
