#!/usr/bin/env python3
"""
API Testing Script
Tests all API endpoints with PostgreSQL database integration
"""

import os
import sys
import requests
import json
import time
from datetime import datetime

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        self.test_user = None
        self.test_note = None
        
    def test_health_check(self):
        """Test API Gateway health check"""
        print("🔍 Testing API Gateway health...")
        
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                print("✅ API Gateway is healthy")
                return True
            else:
                print(f"❌ API Gateway health check failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ API Gateway connection failed: {e}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        print("\n🔍 Testing user registration...")
        
        user_data = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/users/register",
                json=user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ User registration successful")
                self.test_user = response.json()
                print(f"📊 User ID: {self.test_user.get('id')}")
                return True
            else:
                print(f"❌ User registration failed: {response.status_code}")
                print(f"📊 Response: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ User registration error: {e}")
            return False
    
    def test_user_login(self):
        """Test user login"""
        print("\n🔍 Testing user login...")
        
        if not self.test_user:
            print("❌ No test user available")
            return False
        
        login_data = {
            "username": self.test_user["username"],
            "password": "testpassword123"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/users/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ User login successful")
                login_result = response.json()
                self.auth_token = login_result.get("access_token")
                
                # Set authorization header
                self.session.headers.update({
                    "Authorization": f"Bearer {self.auth_token}"
                })
                
                return True
            else:
                print(f"❌ User login failed: {response.status_code}")
                print(f"📊 Response: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ User login error: {e}")
            return False
    
    def test_user_profile(self):
        """Test user profile endpoint"""
        print("\n🔍 Testing user profile...")
        
        try:
            response = self.session.get(
                f"{self.base_url}/users/profile",
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ User profile retrieval successful")
                profile = response.json()
                print(f"📊 User: {profile.get('username')}")
                return True
            else:
                print(f"❌ User profile failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ User profile error: {e}")
            return False
    
    def test_notes_upload(self):
        """Test note upload"""
        print("\n🔍 Testing note upload...")
        
        # Create a simple test file
        test_content = """
        # Test Note
        
        This is a test note for the Notes Microservices application.
        
        ## Features
        - User authentication
        - Note management
        - Study sessions
        - RAG Q&A
        
        ## Database
        This application uses PostgreSQL for data storage.
        All services connect to the same database.
        """
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(test_content)
                temp_file = f.name
            
            # Upload file
            with open(temp_file, 'rb') as f:
                files = {'file': ('test_note.txt', f, 'text/plain')}
                response = self.session.post(
                    f"{self.base_url}/notes/upload",
                    files=files,
                    timeout=30
                )
            
            # Clean up
            os.unlink(temp_file)
            
            if response.status_code == 200:
                print("✅ Note upload successful")
                self.test_note = response.json()
                print(f"📊 Note ID: {self.test_note.get('id')}")
                return True
            else:
                print(f"❌ Note upload failed: {response.status_code}")
                print(f"📊 Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Note upload error: {e}")
            return False
    
    def test_notes_list(self):
        """Test notes listing"""
        print("\n🔍 Testing notes list...")
        
        try:
            response = self.session.get(f"{self.base_url}/notes/", timeout=10)
            
            if response.status_code == 200:
                print("✅ Notes list retrieval successful")
                notes = response.json()
                print(f"📊 Found {len(notes)} notes")
                return True
            else:
                print(f"❌ Notes list failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Notes list error: {e}")
            return False
    
    def test_flashcards(self):
        """Test flashcard generation"""
        print("\n🔍 Testing flashcard generation...")
        
        if not self.test_note:
            print("❌ No test note available")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/sessions/flashcards",
                json={"note_id": self.test_note["id"]},
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ Flashcard generation successful")
                flashcards = response.json()
                print(f"📊 Generated {len(flashcards)} flashcards")
                return True
            else:
                print(f"❌ Flashcard generation failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Flashcard generation error: {e}")
            return False
    
    def test_quiz(self):
        """Test quiz creation"""
        print("\n🔍 Testing quiz creation...")
        
        if not self.test_note:
            print("❌ No test note available")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/sessions/quiz",
                json={
                    "note_id": self.test_note["id"],
                    "title": "Test Quiz"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ Quiz creation successful")
                quiz = response.json()
                print(f"📊 Quiz ID: {quiz.get('id')}")
                return True
            else:
                print(f"❌ Quiz creation failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Quiz creation error: {e}")
            return False
    
    def test_rag_ingest(self):
        """Test RAG document ingestion"""
        print("\n🔍 Testing RAG document ingestion...")
        
        if not self.test_note:
            print("❌ No test note available")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/qa/ingest",
                json={"note_id": self.test_note["id"]},
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ RAG ingestion successful")
                result = response.json()
                print(f"📊 Document ID: {result.get('document_id')}")
                return True
            else:
                print(f"❌ RAG ingestion failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ RAG ingestion error: {e}")
            return False
    
    def test_rag_qa(self):
        """Test RAG Q&A"""
        print("\n🔍 Testing RAG Q&A...")
        
        try:
            response = self.session.post(
                f"{self.base_url}/qa/ask",
                json={"question": "What database does this application use?"},
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ RAG Q&A successful")
                qa_result = response.json()
                print(f"📊 Answer: {qa_result.get('answer', '')[:100]}...")
                return True
            else:
                print(f"❌ RAG Q&A failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ RAG Q&A error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting API Tests")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("User Profile", self.test_user_profile),
            ("Notes Upload", self.test_notes_upload),
            ("Notes List", self.test_notes_list),
            ("Flashcards", self.test_flashcards),
            ("Quiz", self.test_quiz),
            ("RAG Ingestion", self.test_rag_ingest),
            ("RAG Q&A", self.test_rag_qa)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                results[test_name] = False
            
            time.sleep(1)  # Small delay between tests
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 API Test Results Summary:")
        
        passed = 0
        for test_name, result in results.items():
            status = '✅ PASS' if result else '❌ FAIL'
            print(f"🧪 {test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\n📈 Overall: {passed}/{len(tests)} tests passed")
        
        if passed == len(tests):
            print("🎉 All API tests passed! The application is working correctly.")
        else:
            print("⚠️  Some API tests failed. Please check the errors above.")
        
        return passed == len(tests)

def main():
    """Main function"""
    # Check if services are running
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    print(f"🔗 Testing API at: {base_url}")
    
    # Create tester and run tests
    tester = APITester(base_url)
    success = tester.run_all_tests()
    
    return success

if __name__ == "__main__":
    import tempfile  # Import here to avoid issues if not available
    
    success = main()
    sys.exit(0 if success else 1)
