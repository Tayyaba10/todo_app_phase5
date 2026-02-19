---
name: containerize-frontend-backend
description: Containerize frontend and backend applications using Docker for consistent deployment and development.
---

# Containerize Frontend & Backend

## Instructions

1. **Dockerfile Creation**
   - Create separate Dockerfiles for frontend and backend
   - Define base image and dependencies
   - Set working directory and copy source code
   - Expose necessary ports and define entrypoint

2. **Docker Compose Setup**
   - Use `docker-compose.yml` to define multi-container setup
   - Configure services, networks, and volumes
   - Set environment variables for both frontend and backend
   - Ensure proper port mapping and dependencies

3. **Building & Running Containers**
   - Build images using `docker build` or `docker-compose build`
   - Run containers locally with `docker run` or `docker-compose up`
   - Check logs and ensure containers communicate correctly
   - Rebuild containers after code changes

4. **Best Practices**
   - Keep Dockerfiles lean and minimal
   - Use `.dockerignore` to reduce build context
   - Use environment variables for sensitive data
   - Separate dev, staging, and production configurations
   - Tag images properly for versioning
   - Use healthchecks to monitor container status

## Example Structure

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

### Frontend Dockerfile
FROM node:20-alpine

WORKDIR /src
COPY package.json yarn.lock ./
RUN yarn install
COPY . .

EXPOSE 3000
CMD ["yarn", "dev"]