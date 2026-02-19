# Quickstart Guide: Todo Chatbot Kubernetes Deployment

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

3. **Clone Repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd todo_app_phase4
   ```

## Deployment Steps

### 1. Containerize Applications

Using the Docker Agent to create optimized container images:

```bash
# Build frontend container
docker build -t todo-chatbot-frontend:latest -f ./frontend/Dockerfile .

# Build backend container
docker build -t todo-chatbot-backend:latest -f ./backend/Dockerfile .
```

### 2. Prepare Helm Chart

The Helm chart for the Todo Chatbot application is located in `./charts/todo-chatbot/`. Customize the `values.yaml` file as needed for your environment.

### 3. Deploy to Kubernetes

```bash
# Navigate to the Helm chart directory
cd charts/todo-chatbot

# Install the Helm chart
helm install todo-chatbot . --namespace todo-chatbot --create-namespace
```

### 4. Verify Deployment

```bash
# Check if pods are running
kubectl get pods -n todo-chatbot

# Check services
kubectl get svc -n todo-chatbot

# Check if application is accessible
minikube service todo-chatbot-frontend -n todo-chatbot --url
```

### 5. Access Application

```bash
# Get the frontend URL
minikube service todo-chatbot-frontend -n todo-chatbot

# Or port forward for direct access
kubectl port-forward -n todo-chatbot svc/todo-chatbot-frontend 3000:3000
```

## Monitoring and Observability

1. **View Application Logs**:
   ```bash
   kubectl logs -n todo-chatbot -l app=todo-chatbot-backend
   kubectl logs -n todo-chatbot -l app=todo-chatbot-frontend
   ```

2. **Check Resource Usage**:
   ```bash
   kubectl top pods -n todo-chatbot
   ```

3. **Monitor Health**:
   ```bash
   kubectl get events -n todo-chatbot
   ```

## Scaling the Application

```bash
# Scale frontend replicas
kubectl scale -n todo-chatbot deployment/todo-chatbot-frontend --replicas=3

# Scale backend replicas
kubectl scale -n todo-chatbot deployment/todo-chatbot-backend --replicas=2
```

## Cleanup

```bash
# Uninstall the Helm release
helm uninstall todo-chatbot -n todo-chatbot

# Delete the namespace
kubectl delete namespace todo-chatbot
```

## Troubleshooting

1. **Pods not starting**:
   ```bash
   kubectl describe -n todo-chatbot pods -l app=todo-chatbot
   ```

2. **Service not accessible**:
   ```bash
   kubectl get endpoints -n todo-chatbot -l app=todo-chatbot
   ```

3. **Resource constraints**:
   ```bash
   kubectl describe nodes
   ```