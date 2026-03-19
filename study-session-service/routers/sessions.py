from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
import random
import re
from models import get_db, Flashcard, Quiz, StudySession
from schemas import (
    FlashcardCreate, FlashcardResponse, 
    QuizCreate, QuizResponse, Question,
    StudySessionBase, StudySessionResponse, 
    FlashcardGenerationRequest, QuizGenerationRequest
)

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)

# Service URLs
NOTES_SERVICE_URL = "http://localhost:8002"
RAG_QA_SERVICE_URL = "http://rag-qa-service:8000"

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

@router.post("/flashcards", response_model=List[FlashcardResponse])
async def create_flashcards(request: FlashcardGenerationRequest, db: Session = Depends(get_db)):
    """
    Generate flashcards from note content
    """
    note = await get_note_content(request.note_id)
    content = note.get("content", "")
    
    if not content:
        raise HTTPException(status_code=400, detail="No content available for flashcard generation")
    
    # Simple flashcard generation - in production, use RAG service
    flashcards = []
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
    
    if len(sentences) < 2:
        raise HTTPException(status_code=400, detail="Not enough content to generate flashcards")
    
    # Generate flashcards by splitting sentences
    for i in range(min(request.count, len(sentences) // 2)):
        sentence = sentences[i * 2]
        if len(sentence) > 100:
            # Split long sentences
            words = sentence.split()
            question = " ".join(words[:len(words)//2]) + "..."
            answer = " ".join(words[len(words)//2:])
        else:
            question = sentence[:len(sentence)//2] + "..."
            answer = sentence[len(sentence)//2:]
        
        flashcard = Flashcard(
            question=question.strip(),
            answer=answer.strip(),
            user_id=request.user_id,
            note_id=request.note_id
        )
        db.add(flashcard)
        flashcards.append(flashcard)
    
    db.commit()
    
    for flashcard in flashcards:
        db.refresh(flashcard)
    
    return flashcards

@router.get("/flashcards", response_model=List[FlashcardResponse])
async def get_flashcards(user_id: int, note_id: int = None, db: Session = Depends(get_db)):
    """
    Get flashcards for a user, optionally filtered by note
    """
    query = db.query(Flashcard).filter(Flashcard.user_id == user_id)
    if note_id:
        query = query.filter(Flashcard.note_id == note_id)
    flashcards = query.all()
    return flashcards

@router.post("/quiz", response_model=QuizResponse)
async def create_quiz(request: QuizGenerationRequest, db: Session = Depends(get_db)):
    """
    Generate a quiz from note content
    """
    note = await get_note_content(request.note_id)
    content = note.get("content", "")
    
    if not content:
        raise HTTPException(status_code=400, detail="No content available for quiz generation")
    
    # Simple quiz generation - in production, use RAG service
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
    
    if len(sentences) < 3:
        raise HTTPException(status_code=400, detail="Not enough content to generate quiz")
    
    questions = []
    for i in range(min(request.question_count, len(sentences))):
        correct_sentence = sentences[i]
        # Create multiple choice options
        options = [correct_sentence]
        
        # Add distractors (other sentences)
        for j in range(min(3, len(sentences) - 1)):
            if j != i:
                options.append(sentences[j])
        
        # Ensure we have 4 options
        while len(options) < 4:
            options.extend(sentences[:4-len(options)])
        
        options = options[:4]
        random.shuffle(options)
        correct_answer = options.index(correct_sentence)
        
        question = Question(
            question=f"Which of the following statements is correct?",
            options=options,
            correct_answer=correct_answer
        )
        questions.append(question)
    
    quiz = Quiz(
        title=f"Quiz for {note['title']}",
        questions=[q.dict() for q in questions],
        user_id=request.user_id,
        note_id=request.note_id
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    return quiz

@router.get("/quiz", response_model=List[QuizResponse])
async def get_quizzes(user_id: int, note_id: int = None, db: Session = Depends(get_db)):
    """
    Get quizzes for a user, optionally filtered by note
    """
    query = db.query(Quiz).filter(Quiz.user_id == user_id)
    if note_id:
        query = query.filter(Quiz.note_id == note_id)
    quizzes = query.all()
    return quizzes

@router.post("/session", response_model=StudySessionResponse)
async def create_study_session(session: StudySessionBase, db: Session = Depends(get_db)):
    """
    Record a study session
    """
    db_session = StudySession(
        session_type=session.session_type,
        content_id=session.content_id,
        user_id=session.user_id,
        score=session.score,
        total_items=session.total_items,
        time_spent_minutes=session.time_spent_minutes
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/session", response_model=List[StudySessionResponse])
async def get_study_sessions(user_id: int, db: Session = Depends(get_db)):
    """
    Get study sessions for a user
    """
    sessions = db.query(StudySession).filter(StudySession.user_id == user_id).all()
    return sessions
