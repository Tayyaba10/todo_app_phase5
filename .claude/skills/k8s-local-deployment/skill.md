---
name: k8s-local-deployment
description: Deploy and manage applications locally on Kubernetes using Minikube for development and testing.
---

# Local Kubernetes Deployment (Minikube)

## Instructions

1. **Minikube Setup**
   - Install Minikube and kubectl
   - Choose a suitable driver (Docker / VirtualBox)
   - Start local Kubernetes cluster
   - Verify cluster status

2. **Application Deployment**
   - Create Kubernetes manifests (Deployment, Service)
   - Apply YAML files using kubectl
   - Manage pods and replicas
   - Update images and configurations

3. **Service Exposure**
   - Expose services using NodePort or LoadBalancer
   - Access services via Minikube IP
   - Use port-forwarding for local testing

4. **Local Development Workflow**
   - Rebuild images locally
   - Use Minikube Docker daemon
   - Restart deployments after changes
   - Debug pods and logs

## Best Practices
- Use namespaces for organization
- Keep manifests minimal and readable
- Version control Kubernetes YAML files
- Clean up unused resources
- Match local configs with production closely
- Monitor resource usage on local cluster

## Example Structure

### Start Minikube
```bash
minikube start --driver=docker
kubectl get nodes
