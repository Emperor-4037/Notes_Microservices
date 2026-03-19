from fastapi import FastAPI
from routers import notes

app = FastAPI(title="Notes Service", description="Handles study material uploads and retrieval")

app.include_router(notes.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "notes-service"}

@app.get("/")
async def root():
    return {"message": "Notes Service API"}
