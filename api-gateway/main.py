from fastapi import FastAPI, Request, HTTPException, Form, UploadFile, File
from fastapi.responses import HTMLResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional

app = FastAPI(title="Study Assistant API Gateway", description="Gateway routing requests to microservices")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs from environment (or default to localhost for local testing)
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8001")
NOTES_SERVICE_URL = os.getenv("NOTES_SERVICE_URL", "http://localhost:8002")
STUDY_SESSION_SERVICE_URL = os.getenv("STUDY_SESSION_SERVICE_URL", "http://localhost:8003")
RAG_QA_SERVICE_URL = os.getenv("RAG_QA_SERVICE_URL", "http://localhost:8004")

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>API Gateway is running</h1><p>Check <a href='/docs'>/docs</a> for details.</p>"

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "api-gateway"}

# Proxy implementation for demonstration purposes.
# We are manually defining proxied routes for clarity and beginner-friendliness.

async def proxy_request(request: Request, service_url: str, path: str):
    url = f"{service_url}/{path}"
    # This is a very basic proxy implementation.
    # In a real app we would want to forward headers, query params, handling streams properly, etc.
    async with httpx.AsyncClient() as client:
        try:
            # Handle form data and file uploads
            if request.headers.get("content-type", "").startswith("multipart/form-data"):
                # For multipart form data, we need to reconstruct it
                form_data = await request.form()
                files = {}
                data = {}
                
                for key, value in form_data.items():
                    if hasattr(value, 'file'):
                        files[key] = (value.filename, await value.read(), value.content_type)
                    else:
                        data[key] = value
                
                response = await client.post(
                    url=url,
                    files=files,
                    data=data,
                    params=request.query_params
                )
            else:
                req_body = await request.body()
                # Note: We do not forward all headers to avoid Host mismatch or Encoding issues in this simple proxy
                response = await client.request(
                    method=request.method,
                    url=url,
                    content=req_body,
                    params=request.query_params
                )
            
            # Fast return a copy of the response
            from fastapi.responses import Response
            return Response(
                content=response.content,
                status_code=response.status_code,
                # Avoid passing back problematic headers like 'content-encoding': 'gzip' directly 
                # from an internal request if not strictly handling it.
                media_type=response.headers.get("content-type", "application/json")
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Error connecting to backend service: {exc}")

@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_users(request: Request, path: str):
    """Proxy requests starting with /users to the User Service"""
    # E.g., /users/profile -> user-service:8000/profile
    return await proxy_request(request, USER_SERVICE_URL, f"users/{path}")

@app.api_route("/notes/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_notes(request: Request, path: str):
    """Proxy requests starting with /notes to the Notes Service"""
    return await proxy_request(request, NOTES_SERVICE_URL, f"notes/{path}")

@app.api_route("/sessions/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_sessions(request: Request, path: str):
    """Proxy requests starting with /sessions to the Study Session Service"""
    return await proxy_request(request, STUDY_SESSION_SERVICE_URL, f"sessions/{path}")

@app.api_route("/qa/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_qa(request: Request, path: str):
    """Proxy requests starting with /qa to the RAG QA Service"""
    return await proxy_request(request, RAG_QA_SERVICE_URL, f"qa/{path}")
