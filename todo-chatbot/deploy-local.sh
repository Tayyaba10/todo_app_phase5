#!/bin/bash

# Script to deploy the Todo App to a local Minikube environment

set -e  # Exit on any error

echo "🚀 Starting Todo App local deployment..."

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "❌ Minikube is not running. Please start minikube first:"
    echo "   minikube start"
    exit 1
fi

# Enable ingress addon
echo "🔌 Enabling ingress addon..."
minikube addons enable ingress

# Set Docker environment to Minikube
echo "🐳 Setting Docker environment to Minikube..."
eval $(minikube docker-env)

# Build images if they don't exist
echo "🔨 Building Docker images..."
cd ../backend
if ! docker images | grep -q "todo-backend"; then
    echo "Building backend image..."
    docker build -t todo-backend .
else
    echo "Backend image already exists"
fi

cd ../frontend
if ! docker images | grep -q "todo-frontend"; then
    echo "Building frontend image..."
    docker build -t todo-frontend .
else
    echo "Frontend image already exists"
fi

# Go back to the helm chart directory
cd ../todo-chatbot

# Check if the release already exists
if helm status todo-app &> /dev/null; then
    echo "🔄 Upgrading existing deployment..."
    helm upgrade todo-app . -f values-local.yaml
else
    echo "✨ Installing new deployment..."
    helm install todo-app . -f values-local.yaml
fi

echo "✅ Deployment completed!"
echo ""
echo "📋 To access the application:"
echo "1. Get Minikube IP: minikube ip"
echo "2. Add to your hosts file: <MINIKUBE_IP> todo-app.local"
echo "3. Access the app at: http://todo-app.local"
echo ""
echo "📊 Check deployment status: kubectl get pods,svc,ingress"