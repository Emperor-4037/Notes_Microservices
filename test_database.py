#!/usr/bin/env python3
"""
Database Connectivity Test Script
Tests PostgreSQL connectivity and schema initialization
"""

import os
import sys
import psycopg2
from psycopg2 import OperationalError
from urllib.parse import urlparse

def test_database_connection():
    """Test PostgreSQL database connection"""
    print("🔍 Testing PostgreSQL database connection...")
    
    # Default database URL
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/notes_microservices")
    print(f"📍 Database URL: {database_url}")
    
    try:
        # Parse connection parameters
        parsed = urlparse(database_url)
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password
        )
        
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL connected successfully!")
        print(f"📊 Version: {version[0]}")
        
        # Test database exists
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        print(f"🗄️  Current database: {db_name[0]}")
        
        conn.close()
        return True
        
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_schema_initialization():
    """Test database schema initialization"""
    print("\n🔍 Testing database schema...")
    
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/notes_microservices")
    
    try:
        parsed = urlparse(database_url)
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password
        )
        cursor = conn.cursor()
        
        # Check if tables exist
        tables = [
            'users', 'notes', 'flashcards', 'quizzes', 
            'study_sessions', 'documents', 'document_chunks'
        ]
        
        existing_tables = []
        for table in tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, (table,))
            exists = cursor.fetchone()[0]
            if exists:
                existing_tables.append(table)
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
        
        # Check foreign key constraints
        cursor.execute("""
            SELECT constraint_name, table_name 
            FROM information_schema.table_constraints 
            WHERE constraint_type = 'FOREIGN KEY';
        """)
        fk_constraints = cursor.fetchall()
        print(f"🔗 Foreign key constraints: {len(fk_constraints)}")
        
        # Check indexes
        cursor.execute("""
            SELECT indexname, tablename 
            FROM pg_indexes 
            WHERE schemaname = 'public';
        """)
        indexes = cursor.fetchall()
        print(f"📋 Indexes: {len(indexes)}")
        
        conn.close()
        
        if len(existing_tables) == len(tables):
            print("✅ All required tables exist!")
            return True
        else:
            print(f"⚠️  Missing {len(tables) - len(existing_tables)} tables")
            return False
            
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False

def test_service_models():
    """Test service model imports and database setup"""
    print("\n🔍 Testing service models...")
    
    services = [
        'user-service',
        'notes-service', 
        'study-session-service',
        'rag-qa-service'
    ]
    
    results = {}
    
    for service in services:
        try:
            print(f"🧪 Testing {service}...")
            
            # Add service directory to Python path
            service_path = os.path.join(os.getcwd(), service)
            if service_path not in sys.path:
                sys.path.insert(0, service_path)
            
            # Try to import models
            if service == 'user-service':
                import models
                print(f"✅ {service} - Models imported successfully")
                
                # Test database setup
                try:
                    models.engine.connect()
                    print(f"✅ {service} - Database connection successful")
                    results[service] = True
                except Exception as e:
                    print(f"❌ {service} - Database connection failed: {e}")
                    results[service] = False
                    
            elif service == 'notes-service':
                import models
                print(f"✅ {service} - Models imported successfully")
                
                try:
                    models.engine.connect()
                    print(f"✅ {service} - Database connection successful")
                    results[service] = True
                except Exception as e:
                    print(f"❌ {service} - Database connection failed: {e}")
                    results[service] = False
                    
            elif service == 'study-session-service':
                import models
                print(f"✅ {service} - Models imported successfully")
                
                try:
                    models.engine.connect()
                    print(f"✅ {service} - Database connection successful")
                    results[service] = True
                except Exception as e:
                    print(f"❌ {service} - Database connection failed: {e}")
                    results[service] = False
                    
            elif service == 'rag-qa-service':
                import models
                print(f"✅ {service} - Models imported successfully")
                
                try:
                    models.engine.connect()
                    print(f"✅ {service} - Database connection successful")
                    results[service] = True
                except Exception as e:
                    print(f"❌ {service} - Database connection failed: {e}")
                    results[service] = False
            
        except ImportError as e:
            print(f"❌ {service} - Import failed: {e}")
            results[service] = False
        except Exception as e:
            print(f"❌ {service} - Unexpected error: {e}")
            results[service] = False
    
    return results

def main():
    """Main test function"""
    print("🚀 Starting PostgreSQL Migration Tests")
    print("=" * 50)
    
    # Test 1: Database Connection
    connection_ok = test_database_connection()
    
    if not connection_ok:
        print("\n❌ Database connection failed. Please check:")
        print("   - PostgreSQL is running")
        print("   - DATABASE_URL environment variable is set")
        print("   - Database credentials are correct")
        return False
    
    # Test 2: Schema Initialization
    schema_ok = test_schema_initialization()
    
    # Test 3: Service Models
    service_results = test_service_models()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"🔗 Database Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"🗄️  Schema Initialization: {'✅ PASS' if schema_ok else '❌ FAIL'}")
    
    for service, result in service_results.items():
        status = '✅ PASS' if result else '❌ FAIL'
        print(f"🧪 {service}: {status}")
    
    # Overall result
    all_passed = connection_ok and schema_ok and all(service_results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! PostgreSQL migration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
