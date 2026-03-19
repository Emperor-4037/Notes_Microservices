# Study Assistant Platform

A fully functional microservices project consisting of five backend microservices and a frontend, all designed to support an AI-driven Retrieval-Augmented Generation (RAG) study system. 

## Architecture Overview
The platform contains the following components:
1. **Frontend App:** A beautiful, responsive UI built with React, Vite, and custom CSS.
2. **API Gateway:** A FastAPI reverse proxy that routes traffic to correct services.
3. **User Service:** A FastAPI service for user profiles and JWT authentication.
4. **Notes Service:** A FastAPI service for managing study materials with file upload support.
5. **Study Session Service:** A FastAPI service for handling study features like flashcards and quizzes.
6. **RAG QA Service:** A FastAPI service with vector embeddings for AI-driven answering from notes.

All backend services are written in Python with **FastAPI** and include complete database integration.

## Features Implemented

### User Service
- User registration with password hashing
- JWT-based authentication
- User profile management
- SQLite database with SQLAlchemy

### Notes Service
- File upload support (PDF, text files)
- CRUD operations for notes
- Local file storage
- Database metadata management

### Study Session Service
- Automatic flashcard generation from notes
- Quiz creation with multiple-choice questions
- Study session tracking and scoring
- Integration with notes service

### RAG QA Service
- Document ingestion and chunking
- Vector embeddings using sentence-transformers
- Similarity search and retrieval
- Question answering with context

### API Gateway
- Request routing to all microservices
- File upload handling
- CORS support
- Error handling

## How to Run Locally

### Prerequisites
- Docker and Docker Compose installed.
- (If running manually) Python 3.10+ and Node.js.

### Using Docker Compose
1. Ensure Docker is running.
2. In the root of this repository, run:
```bash
docker compose up --build
```
3. Navigate to `http://localhost:3000` to access the Frontend.
4. Navigate to `http://localhost:8000/docs` to access the API Gateway documentation.

### Manual Setup
If you prefer to run services individually:

1. **User Service:**
```bash
cd user-service
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. **Notes Service:**
```bash
cd notes-service
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

3. **Study Session Service:**
```bash
cd study-session-service
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

4. **RAG QA Service:**
```bash
cd rag-qa-service
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

5. **API Gateway:**
```bash
cd api-gateway
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

6. **Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### User Service (via Gateway)
- `POST /users/register` - Register new user
- `POST /users/login` - User login
- `GET /users/profile` - Get user profile (requires auth)

### Notes Service (via Gateway)
- `POST /notes/upload` - Upload note file
- `GET /notes/` - Get all notes (optional user_id filter)
- `GET /notes/{id}` - Get specific note
- `PUT /notes/{id}` - Update note
- `DELETE /notes/{id}` - Delete note

### Study Session Service (via Gateway)
- `POST /sessions/flashcards` - Generate flashcards
- `GET /sessions/flashcards` - Get flashcards
- `POST /sessions/quiz` - Create quiz
- `GET /sessions/quiz` - Get quizzes
- `POST /sessions/session` - Record study session
- `GET /sessions/session` - Get study sessions

### RAG QA Service (via Gateway)
- `POST /qa/ingest` - Ingest document for RAG
- `POST /qa/ask` - Ask question
- `GET /qa/documents` - Get all documents
- `GET /qa/documents/{id}/chunks` - Get document chunks

## Database Schema

Each service uses its own SQLite database:
- **User Service:** `users.db` with `users` table
- **Notes Service:** `notes.db` with `notes` table
- **Study Session Service:** `study_sessions.db` with `flashcards`, `quizzes`, `study_sessions` tables
- **RAG QA Service:** `rag_qa.db` with `documents`, `document_chunks` tables

## Next Steps for Production
- Replace SQLite with PostgreSQL or MySQL
- Implement proper secret management
- Add monitoring and logging
- Set up CI/CD pipeline
- Configure production-ready reverse proxy
- Add rate limiting and security measures
- Scale services with container orchestration
