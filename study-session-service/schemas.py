from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FlashcardBase(BaseModel):
    question: str
    answer: str
    note_id: int

class FlashcardCreate(FlashcardBase):
    user_id: int

class FlashcardResponse(FlashcardBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Question(BaseModel):
    question: str
    options: List[str]
    correct_answer: int

class QuizBase(BaseModel):
    title: str
    note_id: int

class QuizCreate(QuizBase):
    user_id: int
    questions: List[Question]

class QuizResponse(QuizBase):
    id: int
    user_id: int
    questions: List[Question]
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudySessionBase(BaseModel):
    session_type: str
    content_id: int
    user_id: int
    score: int
    total_items: int
    time_spent_minutes: int

class StudySessionResponse(StudySessionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class FlashcardGenerationRequest(BaseModel):
    note_id: int
    user_id: int
    count: int = 5

class QuizGenerationRequest(BaseModel):
    note_id: int
    user_id: int
    question_count: int = 5
