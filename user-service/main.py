from fastapi import FastAPI
from routers import users

app = FastAPI(title="User Service", description="Handles user authentication and profiles")

app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "user-service"}

@app.get("/")
async def root():
    return {"message": "User Service API"}
