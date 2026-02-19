# Phase IV Todo Chatbot - Kubernetes Deployment

This project implements the deployment of the Todo Chatbot application on Kubernetes using Helm charts and containerization.

## Architecture

The application consists of:
- **Frontend**: Next.js application serving the user interface
- **Backend**: FastAPI application providing the API endpoints
- **Database**: Neon Serverless PostgreSQL (configured externally)

## Containerization

Both frontend and backend applications are containerized using Docker with multi-stage builds for optimization.

### Frontend Docker Image
- Built with Node.js 18 and Next.js
- Uses multi-stage build to optimize size
- Runs as non-root user for security

### Backend Docker Image
- Built with Python 3.11 and FastAPI
- Uses multi-stage build to optimize size
- Runs as non-root user for security

## Kubernetes Deployment

The application is deployed on Kubernetes using Helm charts for packaging and configuration management.

### Helm Chart Features
- Parameterized configuration via values.yaml
- Separated frontend and backend deployments
- Service definitions for internal communication
- Health checks and resource limits
- Secure secret management

## Quick Start

1. **Build Container Images**:
   ```bash
   # Build frontend
   docker build -t todo-chatbot-frontend:latest -f ./frontend/Dockerfile .

   # Build backend
   docker build -t todo-chatbot-backend:latest -f ./backend/Dockerfile .
   ```

2. **Deploy with Helm**:
   ```bash
   # Navigate to the chart directory
   cd todo-chatbot

   # Install the chart
   helm install todo-chatbot . --namespace todo-chatbot --create-namespace
   ```

## Security Considerations

- All containers run as non-root users
- Secrets are managed separately from configuration
- Resource limits are set to prevent abuse
- Health checks ensure service availability

## Monitoring and Observability

- Health endpoints are available at `/health` for both services
- Structured logging is implemented
- Resource usage is monitored through Kubernetes

## Development

To run the applications locally:

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```
