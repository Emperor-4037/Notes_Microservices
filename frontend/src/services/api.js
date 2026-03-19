import axios from 'axios';

// Get the API Gateway URL from environment variables, or default to localhost:8000
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// User Service API calls
export const userApi = {
  register: (userData) => api.post('/users/register', userData),
  login: (credentials) => api.post('/users/login', credentials),
  getProfile: () => api.get('/users/profile'),
};

// Notes Service API calls
export const notesApi = {
  uploadNote: (formData) => api.post('/notes/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getNotes: (userId) => api.get(`/notes/${userId ? `?user_id=${userId}` : ''}`),
  getNote: (id) => api.get(`/notes/${id}`),
  updateNote: (id, data) => api.put(`/notes/${id}`, data),
  deleteNote: (id) => api.delete(`/notes/${id}`),
};

// Study Session Service API calls
export const sessionApi = {
  createFlashcards: (data) => api.post('/sessions/flashcards', data),
  getFlashcards: (userId, noteId) => api.get(`/sessions/flashcards${userId ? `?user_id=${userId}` : ''}${noteId ? `&note_id=${noteId}` : ''}`),
  createQuiz: (data) => api.post('/sessions/quiz', data),
  getQuizzes: (userId, noteId) => api.get(`/sessions/quiz${userId ? `?user_id=${userId}` : ''}${noteId ? `&note_id=${noteId}` : ''}`),
  createStudySession: (sessionData) => api.post('/sessions/session', sessionData),
  getStudySessions: (userId) => api.get(`/sessions/session${userId ? `?user_id=${userId}` : ''}`),
};

// RAG QA Service API calls
export const qaApi = {
  ingestDocument: (noteId) => api.post('/qa/ingest', { note_id: noteId }),
  askQuestion: (question, noteId, topK = 3) => api.post('/qa/ask', { 
    question, 
    note_id: noteId,
    top_k: topK 
  }),
  getDocuments: () => api.get('/qa/documents'),
  getDocumentChunks: (documentId) => api.get(`/qa/documents/${documentId}/chunks`),
};

export default api;
