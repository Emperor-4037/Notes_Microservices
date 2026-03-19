from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import aiofiles
from models import get_db, Note
from schemas import NoteCreate, NoteResponse, NoteUpdate, FileUploadResponse

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=FileUploadResponse)
async def upload_note(
    file: UploadFile = File(...),
    title: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload a file and create a note
    """
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content_bytes = await file.read()
        await f.write(content_bytes)
    
    # Read file content for text files
    content_text = ""
    if file.content_type.startswith('text/'):
        content_text = content_bytes.decode('utf-8', errors='ignore') if isinstance(content_bytes, bytes) else content_bytes
    
    # Create note in database
    db_note = Note(
        title=title,
        content=content_text,
        file_path=file_path,
        file_type=file.content_type,
        user_id=user_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    return FileUploadResponse(
        message="File uploaded successfully",
        note=db_note
    )

@router.get("/", response_model=List[NoteResponse])
async def get_notes(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get all notes, optionally filtered by user_id
    """
    query = db.query(Note)
    if user_id:
        query = query.filter(Note.user_id == user_id)
    notes = query.all()
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Get a specific note by ID
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a note
    """
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    for field, value in note_update.dict(exclude_unset=True).items():
        setattr(db_note, field, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Delete a note
    """
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Delete file if exists
    if db_note.file_path and os.path.exists(db_note.file_path):
        os.remove(db_note.file_path)
    
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}
