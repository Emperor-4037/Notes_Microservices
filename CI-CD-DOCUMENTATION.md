# CI/CD Pipeline Documentation

## Overview

This project includes a comprehensive CI/CD pipeline that automates the entire process from code changes to deployment. The pipeline is designed to ensure code quality, test functionality, and deploy the microservices application reliably.

## Pipeline Triggers

The CI/CD pipeline can be triggered in multiple ways:

1. **Automatic on Push**: Automatically runs when code is pushed to the `main` branch
2. **Automatic on Pull Request**: Runs when pull requests are created/updated targeting the `main` branch
3. **Manual Trigger**: Can be manually triggered from the GitHub Actions UI using "workflow_dispatch"

## Pipeline Stages

### 1. Lint and Test (`lint-and-test` job)

- **Python Setup**: Sets up Python 3.11 environment
- **Dependency Installation**: Installs linting tools (flake8, black, isort) and service dependencies
- **Code Linting**: Runs code quality checks on all Python services
- **Unit Tests**: Executes unit tests for each microservice

### 2. Build Services (`build-services` job)

- **Docker Buildx**: Sets up advanced Docker building capabilities
- **Container Registry Login**: Logs into GitHub Container Registry (ghcr.io)
- **Image Building**: Builds Docker images for all services:
  - API Gateway
  - User Service
  - Notes Service
  - Study Session Service
  - RAG QA Service
  - Frontend
- **Image Pushing**: Pushes images to container registry (only on non-PR runs)

### 3. Integration Testing (`integration-test` job)

- **Docker Compose Setup**: Installs and configures Docker Compose
- **Production Compose File**: Creates a production-ready compose file with built images
- **Service Startup**: Starts all services using Docker Compose
- **Health Checks**: Performs comprehensive health checks on all services
- **Cleanup**: Cleans up resources after testing

### 4. Deployment (`deploy` job)

- **Production Deployment**: Deploys to production environment (only on main branch pushes)
- **Smoke Tests**: Runs post-deployment smoke tests
- **Environment Protection**: Uses GitHub environments for deployment safety

### 5. Notifications (`notify` job)

- **Success Notification**: Sends success notifications
- **Failure Notification**: Sends failure notifications for debugging

## Local Development

### Quick Start

To run the entire pipeline locally:

**Windows:**
```bash
run-pipeline.bat
```

**Linux/Mac:**
```bash
chmod +x run-pipeline.sh
./run-pipeline.sh
```

### Local Pipeline Features

The local pipeline script provides:

- **Prerequisites Check**: Verifies Docker, Docker Compose, and Python are installed
- **Linting and Testing**: Runs the same linting and tests as the CI pipeline
- **Docker Image Building**: Builds all service images locally
- **Integration Testing**: Starts services and performs health checks
- **Interactive Mode**: Allows you to keep services running for manual testing
- **Cleanup**: Automatically cleans up temporary files and containers

## Service Endpoints

When running locally, services are available at:

- **API Gateway**: http://localhost:8000
- **User Service**: http://localhost:8001
- **Notes Service**: http://localhost:8002
- **Study Session Service**: http://localhost:8003
- **RAG QA Service**: http://localhost:8004
- **Frontend**: http://localhost:3000

## Container Registry

Images are stored in GitHub Container Registry:
- Registry: `ghcr.io`
- Repository: `{your-username}/{repository-name}`
- Image Format: `ghcr.io/{username}/{repo}/{service}:{git-sha}`

## Environment Variables

The pipeline uses the following environment variables:

- `REGISTRY`: Container registry URL (ghcr.io)
- `IMAGE_NAME`: Repository name for images
- `GITHUB_TOKEN`: Authentication token for container registry

## Deployment Configuration

### Production Deployment

The deployment stage is configured to:

1. **Only run on main branch pushes**
2. **Use GitHub environments for protection**
3. **Require manual approval (if configured)**
4. **Run smoke tests after deployment**

### Custom Deployment

To customize deployment for your infrastructure:

1. Update the `deploy` job in `.github/workflows/main.yml`
2. Add your deployment commands (Kubernetes, cloud provider, etc.)
3. Configure environment-specific variables
4. Add appropriate secrets for authentication

## Monitoring and Health Checks

### Health Check Endpoints

Each service should implement health check endpoints:

- `/health` - Primary health check endpoint
- `/` - Basic service availability
- `/docs` - API documentation (FastAPI)

### Integration Test Health Checks

The pipeline tests service health by:

1. **Waiting for services to start** (30 seconds)
2. **Attempting to connect to each service** (10 attempts, 5-second intervals)
3. **Testing multiple endpoints** (/health, /, /docs)
4. **Reporting service status**

## Troubleshooting

### Common Issues

1. **Docker Build Failures**:
   - Check Dockerfile syntax
   - Verify base images exist
   - Check for missing dependencies

2. **Health Check Failures**:
   - Services may need more startup time
   - Check service logs for errors
   - Verify port configurations

3. **Linting Failures**:
   - Run linting tools locally to fix issues
   - Check Python code formatting

### Debugging

To debug pipeline issues:

1. **Check GitHub Actions logs** for detailed error messages
2. **Run the local pipeline** to reproduce issues
3. **Examine service logs** using `docker-compose logs`
4. **Test services individually** before running the full pipeline

## Best Practices

1. **Commit frequently** to catch issues early
2. **Run local pipeline** before pushing
3. **Monitor pipeline execution** for performance
4. **Keep dependencies updated** in requirements.txt files
5. **Implement proper health checks** in all services
6. **Use environment-specific configurations**

## Security Considerations

- **GitHub Token**: Automatically provided by GitHub Actions
- **Container Registry**: Uses GitHub's built-in registry
- **Environment Protection**: Deployments use GitHub environments
- **Secrets Management**: Store sensitive data in GitHub Secrets

## Future Enhancements

Potential improvements to the pipeline:

1. **Automated Security Scanning**
2. **Performance Testing**
3. **Multi-Environment Deployments** (staging, production)
4. **Rollback Capabilities**
5. **Advanced Monitoring and Alerting**
6. **Database Migration Automation**
