---
name: cicd-skill
description: Automate build, test, and deployment pipelines using GitHub Actions, Docker, container registries, and Helm.
---

# CI/CD Skill

## Instructions

1. **GitHub Actions Workflows**
   - Create workflow files in `.github/workflows/`
   - Trigger pipelines on push, pull request, or release
   - Define separate jobs for build, test, and deploy
   - Use environment variables and secrets securely

2. **Docker Image Builds**
   - Build images for frontend and backend
   - Use multi-stage builds for smaller images
   - Tag images with version or commit SHA
   - Push images to container registry

3. **Container Registry Management**
   - Use registries like GitHub Container Registry, Docker Hub, or cloud registries
   - Authenticate using secure tokens or secrets
   - Maintain versioned image tags
   - Clean up unused or old images

4. **Helm Deployments**
   - Package applications as Helm charts
   - Update image tags dynamically in values files
   - Deploy to Kubernetes clusters using Helm
   - Support rolling updates and rollbacks

5. **Pipeline Automation**
   - Run tests automatically before builds
   - Deploy to staging before production
   - Use environment-based deployment rules
   - Add notifications for pipeline status

## Best Practices
- Keep pipelines fast and modular
- Use caching for dependencies
- Store secrets securely in GitHub Secrets
- Tag images consistently
- Separate staging and production deployments
- Add rollback strategies for failed deployments

## Example Structure

### GitHub Actions Workflow
```yaml
name: CI Pipeline

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t myapp:latest .
