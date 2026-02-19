# Deployment Guide: Todo Chatbot on Kubernetes

## Overview
This guide provides instructions for deploying the Todo Chatbot application on a local Kubernetes cluster using Minikube and Helm charts.

## Prerequisites
- Docker Desktop 4.53+ with Gordon AI enabled
- Minikube installed and running
- Helm 3.x installed
- kubectl installed and configured
- kubectl-ai and Kagent installed (AI-assisted tools)

## Environment Setup

1. **Start Minikube Cluster**:
   ```bash
   minikube start --driver=docker --memory=4g --cpus=2
   ```

2. **Verify Cluster**:
   ```bash
   kubectl cluster-info
   minikube status
   ```

## Containerization

### Building Container Images

1. **Build Frontend Container**:
   ```bash
   cd frontend
   docker build -t todo-chatbot-frontend:latest -f Dockerfile .
   ```

2. **Build Backend Container**:
   ```bash
   cd ../backend
   docker build -t todo-chatbot-backend:latest -f Dockerfile .
   ```

### Optimizing Images with Gordon AI
The Dockerfiles are already optimized following best practices:
- Multi-stage builds to reduce image size
- Non-root users for security
- Layer caching optimization
- Minimal base images

## Helm Chart Deployment

### Installing the Chart

1. **Navigate to Chart Directory**:
   ```bash
   cd ../charts/todo-chatbot
   ```

2. **Install the Helm Chart**:
   ```bash
   helm install todo-chatbot . --namespace todo-chatbot --create-namespace
   ```

3. **Verify Installation**:
   ```bash
   helm list -n todo-chatbot
   ```

### Customizing Values
The `values.yaml` file contains customizable parameters for the deployment. You can override these during installation:

```bash
helm install todo-chatbot . --namespace todo-chatbot --create-namespace \
  --set frontend.replicaCount=2 \
  --set backend.replicaCount=2
```

## Verifying the Deployment

### Check Pods Status
```bash
kubectl get pods -n todo-chatbot
```

### Check Services
```bash
kubectl get svc -n todo-chatbot
```

### Access the Application
```bash
# Get the frontend URL
minikube service todo-chatbot-frontend -n todo-chatbot

# Or port forward for direct access
kubectl port-forward -n todo-chatbot svc/todo-chatbot-frontend 3000:3000
```

## Monitoring and Observability

### Health Checks
Both frontend and backend services have health check endpoints at `/health` that return:
```json
{"status": "healthy"}
```

### Resource Monitoring
Monitor resource usage with:
```bash
kubectl top pods -n todo-chatbot
```

### Logs
Access application logs with:
```bash
kubectl logs -n todo-chatbot -l app.kubernetes.io/component=frontend
kubectl logs -n todo-chatbot -l app.kubernetes.io/component=backend
```

## Scaling the Application

### Manual Scaling
Scale deployments manually:
```bash
# Scale frontend replicas
kubectl scale -n todo-chatbot deployment/todo-chatbot-frontend --replicas=3

# Scale backend replicas
kubectl scale -n todo-chatbot deployment/todo-chatbot-backend --replicas=2
```

### Horizontal Pod Autoscaling
To enable automatic scaling, update the Helm chart values to enable HPA.

## Upgrading the Application

### Updating with Helm
```bash
# Update values in values.yaml or via --set
helm upgrade todo-chatbot . --namespace todo-chatbot
```

### Rolling Updates
The Helm chart is configured for rolling updates to ensure zero downtime during deployments.

## Cleanup

### Uninstalling the Application
```bash
helm uninstall todo-chatbot -n todo-chatbot
kubectl delete namespace todo-chatbot
```

## Troubleshooting

### Common Issues

1. **Pods Not Starting**:
   ```bash
   kubectl describe -n todo-chatbot pods -l app.kubernetes.io/name=todo-chatbot
   ```

2. **Service Not Accessible**:
   ```bash
   kubectl get endpoints -n todo-chatbot -l app.kubernetes.io/name=todo-chatbot
   ```

3. **Resource Constraints**:
   ```bash
   kubectl describe nodes
   ```

### Debugging Commands
- Check events: `kubectl get events -n todo-chatbot --sort-by='.lastTimestamp'`
- Port forward for debugging: `kubectl port-forward -n todo-chatbot pod/<pod-name> <local-port>:<container-port>`

## Security Considerations

- All containers run as non-root users
- Secrets are managed separately from configuration
- Resource limits prevent abuse
- Network policies can be added for additional security
- Regular security scanning should be implemented in CI/CD pipelines