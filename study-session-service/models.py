from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Flashcard(Base):
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    user_id = Column(Integer, index=True)
    note_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    questions = Column(JSON)  # Store quiz questions as JSON
    user_id = Column(Integer, index=True)
    note_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_type = Column(String)  # 'flashcard' or 'quiz'
    content_id = Column(Integer)  # flashcard_id or quiz_id
    user_id = Column(Integer, index=True)
    score = Column(Integer)
    total_items = Column(Integer)
    time_spent_minutes = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/notes_microservices")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)
