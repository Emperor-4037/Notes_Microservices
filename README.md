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
7. **PostgreSQL Database:** Centralized database for all microservices.

All backend services are written in Python with **FastAPI** and include complete database integration with PostgreSQL.

## Features Implemented

### User Service
- User registration with password hashing
- JWT-based authentication
- User profile management
- PostgreSQL database with SQLAlchemy

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

## Database Setup

The application now uses PostgreSQL as the centralized database. The database schema includes:

### Tables:
- **users:** User accounts and profiles
- **notes:** Study materials and metadata
- **flashcards:** Generated flashcards from notes
- **quizzes:** Quiz questions and answers
- **study_sessions:** Study session tracking
- **documents:** RAG document storage
- **document_chunks:** Document chunks for vector search

### Database Configuration:
- **Database Name:** `notes_microservices`
- **Default User:** `postgres`
- **Connection:** Configurable via `DATABASE_URL` environment variable

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
5. PostgreSQL will be available on `localhost:5432`

### Manual Setup
If you prefer to run services individually:

1. **Start PostgreSQL:**
```bash
docker run --name postgres-notes -e POSTGRES_DB=notes_microservices -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
```

2. **Initialize Database:**
```bash
psql -h localhost -U postgres -d notes_microservices -f init-db.sql
```

3. **User Service:**
```bash
cd user-service
pip install -r requirements.txt
DATABASE_URL=postgresql://postgres:password@localhost:5432/notes_microservices uvicorn main:app --host 0.0.0.0 --port 8000
```

4. **Notes Service:**
```bash
cd notes-service
pip install -r requirements.txt
DATABASE_URL=postgresql://postgres:password@localhost:5432/notes_microservices uvicorn main:app --host 0.0.0.0 --port 8000
```

5. **Study Session Service:**
```bash
cd study-session-service
pip install -r requirements.txt
DATABASE_URL=postgresql://postgres:password@localhost:5432/notes_microservices uvicorn main:app --host 0.0.0.0 --port 8000
```

6. **RAG QA Service:**
```bash
cd rag-qa-service
pip install -r requirements.txt
DATABASE_URL=postgresql://postgres:password@localhost:5432/notes_microservices uvicorn main:app --host 0.0.0.0 --port 8000
```

7. **API Gateway:**
```bash
cd api-gateway
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

8. **Frontend:**
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

All services now use a centralized PostgreSQL database with the following tables:
- **users:** User accounts with authentication data
- **notes:** Study materials with file metadata
- **flashcards:** Generated flashcards linked to notes
- **quizzes:** Quiz questions stored as JSON
- **study_sessions:** Session tracking and scoring
- **documents:** RAG document storage
- **document_chunks:** Text chunks with vector embeddings

## CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline with:
- **Linting and Testing:** Code quality checks and unit tests
- **Database Integration:** PostgreSQL setup and testing
- **Docker Builds:** Automated container builds
- **Integration Tests:** Full stack testing with database
- **Deployment:** Automated deployment to production

### Pipeline Stages:
1. **Lint and Test:** Code formatting, linting, and unit tests with PostgreSQL
2. **Build Services:** Docker container builds for all services
3. **Integration Test:** Full stack testing with PostgreSQL
4. **Deploy:** Production deployment
5. **Notify:** Success/failure notifications

## Kubernetes Deployment

The project includes Kubernetes manifests for production deployment:
- **PostgreSQL:** Persistent database with ConfigMaps
- **Microservices:** All services with PostgreSQL connectivity
- **Services:** Load balancers and internal networking
- **Volumes:** Persistent storage for database

### Deployment Commands:
```bash
# Create namespace
kubectl create namespace notes-microservices

# Deploy PostgreSQL
kubectl apply -f k8s/postgres.yaml

# Deploy all services
kubectl apply -f k8s/user-service.yaml
kubectl apply -f k8s/notes-service.yaml
kubectl apply -f k8s/study-session-service.yaml
kubectl apply -f k8s/rag-qa-service.yaml
kubectl apply -f k8s/api-gateway.yaml
kubectl apply -f k8s/frontend.yaml
```

## Environment Variables

### Database Configuration:
- `DATABASE_URL`: PostgreSQL connection string
- `POSTGRES_DB`: Database name (default: notes_microservices)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password

### Service URLs:
- `USER_SERVICE_URL`: User service endpoint
- `NOTES_SERVICE_URL`: Notes service endpoint
- `STUDY_SESSION_SERVICE_URL`: Study session service endpoint
- `RAG_QA_SERVICE_URL`: RAG QA service endpoint

## Production Considerations

- ✅ **PostgreSQL Database:** Production-ready database
- ✅ **CI/CD Pipeline:** Automated testing and deployment
- ✅ **Kubernetes Support:** Container orchestration
- ✅ **Environment Configuration:** Flexible configuration
- ✅ **Health Checks:** Service monitoring
- ✅ **Persistent Storage:** Database persistence

### Next Steps:
- Implement proper secret management
- Add monitoring and logging
- Set up production reverse proxy
- Add rate limiting and security measures
- Configure auto-scaling
- Set up backup and recovery
