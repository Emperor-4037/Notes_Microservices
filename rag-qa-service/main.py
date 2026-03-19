from fastapi import FastAPI
from routers import qa

app = FastAPI(title="RAG QA Service", description="AI service to answer questions based on uploaded notes")

app.include_router(qa.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "rag-qa-service"}

@app.get("/")
async def root():
    return {"message": "RAG QA Service API"}
