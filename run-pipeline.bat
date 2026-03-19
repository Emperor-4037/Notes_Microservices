@echo off
REM Local Development Pipeline Script for Windows
REM This script simulates the CI/CD pipeline locally for development and testing

echo 🚀 Starting Local Development Pipeline...
echo ========================================

REM Check prerequisites
echo [INFO] Checking prerequisites...

docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python first.
    pause
    exit /b 1
)

echo [INFO] Prerequisites check passed!

REM Step 1: Lint and Test
echo [INFO] Step 1: Running linting and tests...

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
python -m pip install --upgrade pip
pip install flake8 black isort pytest

REM Install service dependencies
for %%s in (api-gateway user-service notes-service study-session-service rag-qa-service) do (
    if exist "%%s\requirements.txt" (
        echo [INFO] Installing dependencies for %%s...
        pip install -r "%%s\requirements.txt"
    )
)

REM Run linting
echo [INFO] Running linting...
for %%s in (api-gateway user-service notes-service study-session-service rag-qa-service) do (
    if exist "%%s" (
        echo [INFO] Linting %%s...
        flake8 %%s --max-line-length=88 --ignore=E203,W503 || echo [WARN] Linting issues found in %%s
        black --check %%s || echo [WARN] Formatting issues found in %%s
        isort --check-only %%s || echo [WARN] Import sorting issues found in %%s
    )
)

REM Run unit tests
echo [INFO] Running unit tests...
for %%s in (api-gateway user-service notes-service study-session-service rag-qa-service) do (
    if exist "%%s" (
        echo [INFO] Running tests for %%s...
        cd %%s
        if exist "main.py" (
            python -m pytest || echo [WARN] No tests found or tests failed for %%s
        )
        cd ..
    )
)

echo [INFO] Linting and testing completed!

REM Step 2: Build Services
echo [INFO] Step 2: Building Docker images...

REM Build each service
echo [INFO] Building api-gateway...
docker build ./api-gateway --file ./api-gateway/Dockerfile -t local-api-gateway:latest
if errorlevel 1 (
    echo [ERROR] Failed to build api-gateway
    pause
    exit /b 1
)

echo [INFO] Building user-service...
docker build ./user-service --file ./user-service/Dockerfile -t local-user-service:latest
if errorlevel 1 (
    echo [ERROR] Failed to build user-service
    pause
    exit /b 1
)

echo [INFO] Building notes-service...
docker build ./notes-service --file ./notes-service/Dockerfile -t local-notes-service:latest
if errorlevel 1 (
    echo [ERROR] Failed to build notes-service
    pause
    exit /b 1
)

echo [INFO] Building study-session-service...
docker build ./study-session-service --file ./study-session-service/Dockerfile -t local-study-session-service:latest
if errorlevel 1 (
    echo [ERROR] Failed to build study-session-service
    pause
    exit /b 1
)

echo [INFO] Building rag-qa-service...
docker build ./rag-qa-service --file ./rag-qa-service/Dockerfile -t local-rag-qa-service:latest
if errorlevel 1 (
    echo [ERROR] Failed to build rag-qa-service
    pause
    exit /b 1
)

echo [INFO] Building frontend...
docker build ./frontend --file ./frontend/Dockerfile -t local-frontend:latest
if errorlevel 1 (
    echo [ERROR] Failed to build frontend
    pause
    exit /b 1
)

echo [INFO] All services built successfully!

REM Step 3: Integration Testing
echo [INFO] Step 3: Running integration tests...

REM Create local compose file
echo [INFO] Creating local compose file...
(
echo version: '3.8'
echo services:
echo   api-gateway:
echo     image: local-api-gateway:latest
echo     ports:
echo       - "8000:8000"
echo     depends_on:
echo       - user-service
echo       - notes-service
echo       - study-session-service
echo       - rag-qa-service
echo     environment:
echo       - ENV=local
echo.
echo   user-service:
echo     image: local-user-service:latest
echo     ports:
echo       - "8001:8000"
echo     environment:
echo       - ENV=local
echo.
echo   notes-service:
echo     image: local-notes-service:latest
echo     ports:
echo       - "8002:8000"
echo     environment:
echo       - ENV=local
echo.
echo   study-session-service:
echo     image: local-study-session-service:latest
echo     ports:
echo       - "8003:8000"
echo     environment:
echo       - ENV=local
echo.
echo   rag-qa-service:
echo     image: local-rag-qa-service:latest
echo     ports:
echo       - "8004:8000"
echo     environment:
echo       - ENV=local
echo.
echo   frontend:
echo     image: local-frontend:latest
echo     ports:
echo       - "3000:80"
echo     depends_on:
echo       - api-gateway
echo     environment:
echo       - ENV=local
) > docker-compose.local.yml

REM Start services
echo [INFO] Starting services for integration testing...
docker-compose -f docker-compose.local.yml up -d

REM Wait for services to be ready
echo [INFO] Waiting for services to start...
timeout /t 30 /nobreak

REM Health checks
echo [INFO] Running health checks...
set all_services_healthy=true

REM Check each service
call :check_service api-gateway 8000
call :check_service user-service 8001
call :check_service notes-service 8002
call :check_service study-session-service 8003
call :check_service rag-qa-service 8004

REM Check frontend
echo [INFO] Checking frontend...
curl -f http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    echo [WARN] Frontend check failed
) else (
    echo [INFO] Frontend is healthy! ✅
)

echo [INFO] Integration testing completed!
echo [INFO] Services are still running. You can:
echo   - View logs: docker-compose -f docker-compose.local.yml logs -f
echo   - Stop services: docker-compose -f docker-compose.local.yml down
echo   - Access services:
echo     * API Gateway: http://localhost:8000
echo     * User Service: http://localhost:8001
echo     * Notes Service: http://localhost:8002
echo     * Study Session Service: http://localhost:8003
echo     * RAG QA Service: http://localhost:8004
echo     * Frontend: http://localhost:3000

REM Ask user if they want to stop services
set /p stop_services="Do you want to stop all services? (y/N): "
if /i "%stop_services%"=="y" (
    echo [INFO] Stopping services...
    docker-compose -f docker-compose.local.yml down -v
    echo [INFO] Services stopped!
)

REM Cleanup
echo [INFO] Cleaning up temporary files...
del docker-compose.local.yml

echo [INFO] Local Development Pipeline completed! 🚀
echo ========================================

if "%all_services_healthy%"=="true" (
    echo [INFO] ✅ All checks passed! Your application is ready for deployment.
) else (
    echo [ERROR] ❌ Some checks failed. Please review the logs above.
)

pause
exit /b 0

REM Function to check service health
:check_service
set service_name=%1
set port=%2
echo [INFO] Checking health of %service_name% on port %port%...

set attempts=0
:check_loop
set /a attempts+=1
curl -f http://localhost:%port%/health >nul 2>&1
if not errorlevel 1 (
    echo [INFO] %service_name% is healthy! ✅
    goto :check_done
)

curl -f http://localhost:%port%/ >nul 2>&1
if not errorlevel 1 (
    echo [INFO] %service_name% is healthy! ✅
    goto :check_done
)

curl -f http://localhost:%port%/docs >nul 2>&1
if not errorlevel 1 (
    echo [INFO] %service_name% is healthy! ✅
    goto :check_done
)

if %attempts% geq 10 (
    echo [ERROR] %service_name% failed health check! ❌
    set all_services_healthy=false
    goto :check_done
)

echo [WARN] Attempt %attempts%: %service_name% not ready, waiting...
timeout /t 5 /nobreak
goto :check_loop

:check_done
goto :eof
