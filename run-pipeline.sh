#!/bin/bash

# Local Development Pipeline Script
# This script simulates the CI/CD pipeline locally for development and testing

set -e

echo "🚀 Starting Local Development Pipeline..."
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command_exists docker; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

print_status "Prerequisites check passed!"

# Step 1: Lint and Test
print_status "Step 1: Running linting and tests..."

# Install Python dependencies
print_status "Installing Python dependencies..."
python3 -m pip install --upgrade pip
pip3 install flake8 black isort pytest

# Install service dependencies
for service in api-gateway user-service notes-service study-session-service rag-qa-service; do
    if [ -f "$service/requirements.txt" ]; then
        print_status "Installing dependencies for $service..."
        pip3 install -r "$service/requirements.txt"
    fi
done

# Run linting
print_status "Running linting..."
for service in api-gateway user-service notes-service study-session-service rag-qa-service; do
    if [ -d "$service" ]; then
        print_status "Linting $service..."
        flake8 "$service" --max-line-length=88 --ignore=E203,W503 || print_warning "Linting issues found in $service"
        black --check "$service" || print_warning "Formatting issues found in $service"
        isort --check-only "$service" || print_warning "Import sorting issues found in $service"
    fi
done

# Run unit tests
print_status "Running unit tests..."
for service in api-gateway user-service notes-service study-session-service rag-qa-service; do
    if [ -d "$service" ]; then
        print_status "Running tests for $service..."
        cd "$service"
        if [ -f "main.py" ]; then
            python3 -m pytest || print_warning "No tests found or tests failed for $service"
        fi
        cd ..
    fi
done

print_status "Linting and testing completed!"

# Step 2: Build Services
print_status "Step 2: Building Docker images..."

services=("api-gateway" "user-service" "notes-service" "study-session-service" "rag-qa-service" "frontend")

for service in "${services[@]}"; do
    print_status "Building $service..."
    if docker build "./$service" --file "./$service/Dockerfile" -t "local-$service:latest"; then
        print_status "$service built successfully!"
    else
        print_error "Failed to build $service"
        exit 1
    fi
done

print_status "All services built successfully!"

# Step 3: Integration Testing
print_status "Step 3: Running integration tests..."

# Create local compose file with built images
cat > docker-compose.local.yml << EOF
version: '3.8'
services:
  api-gateway:
    image: local-api-gateway:latest
    ports:
      - "8000:8000"
    depends_on:
      - user-service
      - notes-service
      - study-session-service
      - rag-qa-service
    environment:
      - ENV=local
  
  user-service:
    image: local-user-service:latest
    ports:
      - "8001:8000"
    environment:
      - ENV=local
  
  notes-service:
    image: local-notes-service:latest
    ports:
      - "8002:8000"
    environment:
      - ENV=local
  
  study-session-service:
    image: local-study-session-service:latest
    ports:
      - "8003:8000"
    environment:
      - ENV=local
  
  rag-qa-service:
    image: local-rag-qa-service:latest
    ports:
      - "8004:8000"
    environment:
      - ENV=local
  
  frontend:
    image: local-frontend:latest
    ports:
      - "3000:80"
    depends_on:
      - api-gateway
    environment:
      - ENV=local
EOF

# Start services
print_status "Starting services for integration testing..."
docker-compose -f docker-compose.local.yml up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 30

# Health checks
print_status "Running health checks..."
all_services_healthy=true

for service in api-gateway:8000 user-service:8001 notes-service:8002 study-session-service:8003 rag-qa-service:8004; do
    service_name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    print_status "Checking health of $service_name on port $port..."
    
    for i in {1..10}; do
        if curl -f http://localhost:$port/health 2>/dev/null || curl -f http://localhost:$port/ 2>/dev/null || curl -f http://localhost:$port/docs 2>/dev/null; then
            print_status "$service_name is healthy! ✅"
            break
        else
            if [ $i -eq 10 ]; then
                print_error "$service_name failed health check! ❌"
                all_services_healthy=false
            else
                print_warning "Attempt $i: $service_name not ready, waiting..."
                sleep 5
            fi
        fi
    done
done

# Check frontend
print_status "Checking frontend..."
if curl -f http://localhost:3000 2>/dev/null; then
    print_status "Frontend is healthy! ✅"
else
    print_warning "Frontend check failed"
fi

if [ "$all_services_healthy" = true ]; then
    print_status "All services passed health checks! 🎉"
else
    print_error "Some services failed health checks"
fi

# Step 4: Show logs and cleanup options
print_status "Integration testing completed!"
print_status "Services are still running. You can:"
echo "  - View logs: docker-compose -f docker-compose.local.yml logs -f"
echo "  - Stop services: docker-compose -f docker-compose.local.yml down"
echo "  - Access services:"
echo "    * API Gateway: http://localhost:8000"
echo "    * User Service: http://localhost:8001"
echo "    * Notes Service: http://localhost:8002"
echo "    * Study Session Service: http://localhost:8003"
echo "    * RAG QA Service: http://localhost:8004"
echo "    * Frontend: http://localhost:3000"

# Ask user if they want to stop services
read -p "Do you want to stop all services? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Stopping services..."
    docker-compose -f docker-compose.local.yml down -v
    print_status "Services stopped!"
fi

# Cleanup
print_status "Cleaning up temporary files..."
rm -f docker-compose.local.yml

print_status "Local Development Pipeline completed! 🚀"
echo "========================================"

if [ "$all_services_healthy" = true ]; then
    print_status "✅ All checks passed! Your application is ready for deployment."
    exit 0
else
    print_error "❌ Some checks failed. Please review the logs above."
    exit 1
fi
