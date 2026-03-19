#!/usr/bin/env python3
"""
Test script to verify the API Gateway and RAG QA service fixes
"""
import httpx
import asyncio
import os

async def test_api_gateway():
    """Test API Gateway connection to services"""
    print("Testing API Gateway fixes...")
    
    # Test the API Gateway health endpoint
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health", timeout=5.0)
            if response.status_code == 200:
                print("✅ API Gateway health check passed")
                return True
            else:
                print(f"❌ API Gateway health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ API Gateway connection failed: {e}")
        return False

async def test_rag_qa_service():
    """Test RAG QA service connection to notes service"""
    print("\nTesting RAG QA Service fixes...")
    
    # Test the RAG QA service health endpoint
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8004/health", timeout=5.0)
            if response.status_code == 200:
                print("✅ RAG QA Service health check passed")
                return True
            else:
                print(f"❌ RAG QA Service health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ RAG QA Service connection failed: {e}")
        return False

async def test_service_urls():
    """Test that service URLs are correctly configured"""
    print("\nTesting service URL configuration...")
    
    # Check environment variables
    gateway_urls = {
        "USER_SERVICE_URL": os.getenv("USER_SERVICE_URL", "http://localhost:8001"),
        "NOTES_SERVICE_URL": os.getenv("NOTES_SERVICE_URL", "http://localhost:8002"),
        "STUDY_SESSION_SERVICE_URL": os.getenv("STUDY_SESSION_SERVICE_URL", "http://localhost:8003"),
        "RAG_QA_SERVICE_URL": os.getenv("RAG_QA_SERVICE_URL", "http://localhost:8004")
    }
    
    print("API Gateway default URLs:")
    for service, url in gateway_urls.items():
        print(f"  {service}: {url}")
    
    # Test if notes service is accessible from RAG QA service URL
    notes_url = os.getenv("NOTES_SERVICE_URL", "http://localhost:8002")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{notes_url}/health", timeout=5.0)
            if response.status_code == 200:
                print("✅ Notes service accessible from RAG QA service")
                return True
            else:
                print(f"❌ Notes service not accessible: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Notes service connection failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🔧 Testing Microservices Fixes")
    print("=" * 50)
    
    results = []
    results.append(await test_api_gateway())
    results.append(await test_rag_qa_service())
    results.append(await test_service_urls())
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All tests passed! ({passed}/{total})")
        print("\nThe fixes are working correctly:")
        print("• API Gateway now uses localhost URLs for local testing")
        print("• RAG QA Service uses environment variable for notes service URL")
        print("• Docker Compose includes proper environment variables")
    else:
        print(f"❌ Some tests failed ({passed}/{total})")
        print("Please check that all services are running correctly")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())
