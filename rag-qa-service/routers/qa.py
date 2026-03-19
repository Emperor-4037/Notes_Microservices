from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
import os
from models import get_db, Document, DocumentChunk
from schemas import (
    IngestRequest, IngestResponse, 
    QuestionRequest, QuestionResponse, 
    DocumentChunkResponse, DocumentResponse
)
from vector_store import vector_store

router = APIRouter(
    prefix="/qa",
    tags=["qa"]
)

# Service URLs
NOTES_SERVICE_URL = os.getenv("NOTES_SERVICE_URL", "http://localhost:8002")

async def get_note_content(note_id: int):
    """Fetch note content from notes service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{NOTES_SERVICE_URL}/notes/{note_id}")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=404, detail="Note not found")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Notes service unavailable")

@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(request: IngestRequest, db: Session = Depends(get_db)):
    """
    Ingest a document for RAG processing
    """
    # Check if document already exists
    existing_doc = db.query(Document).filter(Document.note_id == request.note_id).first()
    if existing_doc:
        # Remove existing chunks
        db.query(DocumentChunk).filter(DocumentChunk.document_id == existing_doc.id).delete()
        db.delete(existing_doc)
        db.commit()
    
    # Get note content
    note = await get_note_content(request.note_id)
    content = note.get("content", "")
    
    if not content:
        raise HTTPException(status_code=400, detail="No content available for ingestion")
    
    # Create document record
    document = Document(
        note_id=request.note_id,
        title=note.get("title", f"Note {request.note_id}"),
        content=content
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Chunk the text
    chunks = vector_store.chunk_text(content)
    
    if not chunks:
        raise HTTPException(status_code=400, detail="Failed to chunk document content")
    
    # Store chunks with embeddings
    vector_store.store_chunks(document.id, chunks, db)
    
    return IngestResponse(
        message="Document ingested successfully",
        document_id=document.id,
        chunks_created=len(chunks)
    )

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest, db: Session = Depends(get_db)):
    """
    Ask a question using RAG
    """
    # Search for relevant chunks
    similar_chunks = vector_store.search_similar(
        query=request.question,
        note_id=request.note_id,
        top_k=request.top_k,
        db=db
    )
    
    if not similar_chunks:
        raise HTTPException(status_code=404, detail="No relevant information found. Please ingest documents first.")
    
    # Simple context-based answer generation
    context = "\n\n".join([chunk[0].chunk_text for chunk in similar_chunks])
    
    # Generate a simple answer (in production, use a proper LLM)
    answer = generate_simple_answer(request.question, context)
    
    # Convert chunks to response format
    source_chunks = [DocumentChunkResponse(
        id=chunk[0].id,
        document_id=chunk[0].document_id,
        chunk_text=chunk[0].chunk_text,
        chunk_index=chunk[0].chunk_index,
        created_at=chunk[0].created_at
    ) for chunk in similar_chunks]
    
    # Calculate average confidence based on similarity scores
    confidence = sum(chunk[1] for chunk in similar_chunks) / len(similar_chunks)
    
    return QuestionResponse(
        answer=answer,
        sources=source_chunks,
        confidence=min(confidence, 1.0)  # Cap at 1.0
    )

def generate_simple_answer(question: str, context: str) -> str:
    """
    Simple answer generation based on context
    In production, replace this with a proper LLM call
    """
    # This is a very basic implementation
    # In a real application, you would use an LLM like GPT, Claude, etc.
    
    context_sentences = context.split('. ')
    
    # Look for sentences that might contain the answer
    question_words = question.lower().split()
    relevant_sentences = []
    
    for sentence in context_sentences:
        sentence_lower = sentence.lower()
        # Simple relevance check
        if any(word in sentence_lower for word in question_words if len(word) > 3):
            relevant_sentences.append(sentence.strip())
    
    if relevant_sentences:
        answer = "Based on the provided context: " + ". ".join(relevant_sentences[:3])
        if not answer.endswith('.'):
            answer += '.'
        return answer
    else:
        return "I found some relevant information in your notes, but I couldn't generate a specific answer. Try rephrasing your question or checking the context provided."

@router.get("/documents", response_model=list[DocumentResponse])
async def get_documents(db: Session = Depends(get_db)):
    """
    Get all ingested documents
    """
    documents = db.query(Document).all()
    return documents

@router.get("/documents/{document_id}/chunks", response_model=list[DocumentChunkResponse])
async def get_document_chunks(document_id: int, db: Session = Depends(get_db)):
    """
    Get chunks for a specific document
    """
    chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).all()
    return chunks
