---
name: local-docker-testing
description: Test frontend, backend, and full-stack applications locally using Docker containers for consistent development environments.
---

# Local Docker Testing

## Instructions

1. **Setup Local Environment**
   - Install Docker and Docker Compose
   - Use `.env` files for environment variables
   - Prepare separate directories for frontend and backend
   - Ensure ports do not conflict locally

2. **Containerized Testing**
   - Build images for frontend and backend
   - Start containers using `docker run` or `docker-compose up`
   - Use healthchecks to verify container readiness
   - Connect services via Docker networks

3. **Automated Tests**
   - Run unit and integration tests inside containers
   - Map test reports and logs to host
   - Use volume mounts for hot-reloading during development
   - Mock external services if required

4. **Debugging & Logs**
   - Inspect container logs with `docker logs`
   - Attach to running containers for debugging
   - Monitor container status with `docker ps` and `docker stats`
   - Restart or rebuild containers as needed

## Best Practices
- Keep test containers isolated from production
- Use lightweight images for testing
- Version-control Dockerfiles and Compose files
- Automate test runs in CI/CD pipelines
- Clean up unused containers and networks
- Use consistent environment variables across services

## Example Structure

### Docker Compose for Local Testing
```yaml
version: "3.9"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///db.sqlite3
    volumes:
      - ./backend:/app
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
