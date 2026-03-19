from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    note_id: int
    title: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_text: str
    chunk_index: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class IngestRequest(BaseModel):
    note_id: int

class IngestResponse(BaseModel):
    message: str
    document_id: int
    chunks_created: int

class QuestionRequest(BaseModel):
    question: str
    note_id: Optional[int] = None
    top_k: int = 3

class QuestionResponse(BaseModel):
    answer: str
    sources: List[DocumentChunkResponse]
    confidence: float
