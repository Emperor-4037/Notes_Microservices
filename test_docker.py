#!/usr/bin/env python3
"""
Docker Compose Validation Script
Validates Docker Compose configuration and service dependencies
"""

import os
import sys
import subprocess
import time
import requests
from urllib.parse import urlparse

def check_docker_compose():
    """Check if Docker Compose is available"""
    print("🔍 Checking Docker Compose availability...")
    
    try:
        # Try docker compose command
        result = subprocess.run(['docker', 'compose', 'version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Docker Compose is available")
            print(f"📊 Version: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        # Try docker-compose command
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Docker Compose (legacy) is available")
            print(f"📊 Version: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ Docker Compose is not available")
    print("💡 Please install Docker and Docker Compose")
    return False

def validate_compose_file():
    """Validate Docker Compose configuration"""
    print("\n🔍 Validating Docker Compose configuration...")
    
    compose_file = 'docker-compose.yml'
    if not os.path.exists(compose_file):
        print(f"❌ {compose_file} not found")
        return False
    
    try:
        # Validate compose file
        result = subprocess.run(['docker', 'compose', 'config'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Docker Compose configuration is valid")
            return True
        else:
            print(f"❌ Docker Compose configuration error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Docker Compose validation timed out")
        return False
    except Exception as e:
        print(f"❌ Docker Compose validation failed: {e}")
        return False

def test_service_startup():
    """Test service startup with PostgreSQL"""
    print("\n🚀 Testing service startup...")
    
    if not check_docker_compose():
        return False
    
    try:
        # Start services
        print("🔄 Starting Docker Compose services...")
        result = subprocess.run(['docker', 'compose', 'up', '-d'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"❌ Failed to start services: {result.stderr}")
            return False
        
        print("✅ Services started successfully")
        
        # Wait for PostgreSQL to be ready
        print("⏳ Waiting for PostgreSQL to be ready...")
        postgres_ready = False
        for i in range(30):  # Wait up to 30 seconds
            try:
                result = subprocess.run(['docker', 'compose', 'exec', '-T', 'postgres', 'pg_isready', '-U', 'postgres'],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    postgres_ready = True
                    print("✅ PostgreSQL is ready")
                    break
                else:
                    print(f"⏳ Attempt {i+1}: PostgreSQL not ready, waiting...")
                    time.sleep(1)
            except:
                print(f"⏳ Attempt {i+1}: PostgreSQL not ready, waiting...")
                time.sleep(1)
        
        if not postgres_ready:
            print("❌ PostgreSQL failed to start")
            return False
        
        # Wait for services to be ready
        print("⏳ Waiting for services to be ready...")
        time.sleep(30)
        
        # Test service health
        services = {
            'api-gateway': 8000,
            'user-service': 8001,
            'notes-service': 8002,
            'study-session-service': 8003,
            'rag-qa-service': 8004
        }
        
        service_status = {}
        
        for service, port in services.items():
            print(f"🔍 Checking {service} on port {port}...")
            
            for attempt in range(10):  # Try 10 times
                try:
                    response = requests.get(f'http://localhost:{port}/', timeout=5)
                    if response.status_code in [200, 404]:  # 404 is ok, means service is running
                        print(f"✅ {service} is healthy")
                        service_status[service] = True
                        break
                    else:
                        print(f"⏳ Attempt {attempt+1}: {service} not ready (status: {response.status_code})")
                except requests.exceptions.RequestException:
                    print(f"⏳ Attempt {attempt+1}: {service} not ready")
                
                if attempt == 9:
                    print(f"❌ {service} failed to start")
                    service_status[service] = False
                
                time.sleep(2)
        
        # Test database connectivity from services
        print("\n🔍 Testing database connectivity from services...")
        try:
            result = subprocess.run([
                'docker', 'compose', 'exec', '-T', 'user-service', 
                'python', '-c', 
                '''
import os
import psycopg2
try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    count = cursor.fetchone()
    print(f"✅ Database connection successful, users table count: {count[0]}")
    conn.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    exit(1)
                '''
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Database connectivity test passed")
                print(f"📊 Output: {result.stdout.strip()}")
            else:
                print("❌ Database connectivity test failed")
                print(f"📊 Error: {result.stderr}")
        
        except Exception as e:
            print(f"❌ Database connectivity test error: {e}")
        
        return service_status
        
    except subprocess.TimeoutExpired:
        print("❌ Service startup timed out")
        return False
    except Exception as e:
        print(f"❌ Service startup failed: {e}")
        return False

def cleanup_services():
    """Clean up Docker Compose services"""
    print("\n🧹 Cleaning up services...")
    
    try:
        result = subprocess.run(['docker', 'compose', 'down', '-v'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Services cleaned up successfully")
        else:
            print(f"⚠️  Cleanup warning: {result.stderr}")
    except Exception as e:
        print(f"⚠️  Cleanup error: {e}")

def main():
    """Main test function"""
    print("🐳 Docker Compose Validation Tests")
    print("=" * 50)
    
    # Test 1: Docker Compose availability
    if not check_docker_compose():
        print("\n❌ Docker Compose is not available. Skipping remaining tests.")
        return False
    
    # Test 2: Configuration validation
    config_ok = validate_compose_file()
    
    if not config_ok:
        print("\n❌ Docker Compose configuration is invalid. Skipping service tests.")
        return False
    
    # Test 3: Service startup
    try:
        service_results = test_service_startup()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Results Summary:")
        print(f"🔧 Docker Compose: ✅ AVAILABLE")
        print(f"📋 Configuration: {'✅ VALID' if config_ok else '❌ INVALID'}")
        
        for service, status in service_results.items():
            status_text = '✅ HEALTHY' if status else '❌ UNHEALTHY'
            print(f"🧪 {service}: {status_text}")
        
        # Overall result
        all_healthy = all(service_results.values())
        
        if all_healthy:
            print("\n🎉 All services are healthy! Docker Compose setup is working correctly.")
        else:
            print("\n⚠️  Some services are unhealthy. Please check the logs for details.")
        
        return all_healthy
        
    finally:
        # Always cleanup
        cleanup_services()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
