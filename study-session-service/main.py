from fastapi import FastAPI
from routers import sessions

app = FastAPI(title="Study Session Service", description="Handles study tracking, flashcards, and quizzes")

app.include_router(sessions.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "study-session-service"}

@app.get("/")
async def root():
    return {"message": "Study Session Service API"}
