# Todo App Helm Chart

This Helm chart deploys the Todo Chatbot application with both frontend and backend services to Kubernetes.

## Chart Structure

- `backend`: FastAPI backend service
- `frontend`: Next.js frontend service
- Both services are deployed as separate deployments with their own services

## Prerequisites

- Kubernetes cluster (tested with Minikube)
- Helm 3+
- Ingress controller (e.g., nginx-ingress)

## Local Development Setup

### 1. Start Minikube

```bash
minikube start
```

### 2. Enable Ingress addon in Minikube

```bash
minikube addons enable ingress
```

### 3. Set Docker environment to Minikube

```bash
eval $(minikube docker-env)
```

### 4. Build your Docker images locally

Make sure your frontend and backend images are built in the Minikube Docker environment:

```bash
# From your project root
cd backend
docker build -t todo-backend .

cd ../frontend
docker build -t todo-frontend .
```

### 5. Deploy using the local values

```bash
helm install todo-app . -f values-local.yaml
```

### 6. Access the application

Get the Minikube IP and add the host entry to your hosts file:

```bash
minikube ip
```

Add to your hosts file (`/etc/hosts` on Linux/Mac or `C:\Windows\System32\drivers\etc\hosts` on Windows):

```
<MINIKUBE_IP> todo-app.local
```

Then access the application at: http://todo-app.local

## Values Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.enabled` | Enable backend service | `true` |
| `backend.image.repository` | Backend image repository | `"todo-backend"` |
| `backend.image.tag` | Backend image tag | `"latest"` |
| `backend.image.pullPolicy` | Backend image pull policy | `"Never"` (for local) |
| `backend.replicaCount` | Number of backend replicas | `1` |
| `backend.service.port` | Backend service port | `8000` |
| `frontend.enabled` | Enable frontend service | `true` |
| `frontend.image.repository` | Frontend image repository | `"todo-frontend"` |
| `frontend.image.tag` | Frontend image tag | `"latest"` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `"Never"` (for local) |
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `frontend.service.port` | Frontend service port | `3000` |

## Customizing the Deployment

To customize the deployment, create your own `values.yaml` file and override the desired parameters:

```bash
helm install todo-app . -f my-values.yaml
```

## Upgrading the Deployment

```bash
helm upgrade todo-app . -f values-local.yaml
```

## Uninstalling

```bash
helm uninstall todo-app
```

## Troubleshooting

### Check if pods are running:
```bash
kubectl get pods
```

### Check pod logs:
```bash
kubectl logs -l app.kubernetes.io/name=todo-app-backend
kubectl logs -l app.kubernetes.io/name=todo-app-frontend
```

### Check services:
```bash
kubectl get svc
```

### Check ingress:
```bash
kubectl get ingress
```