@echo off
REM Script to deploy the Todo App to a local Minikube environment

echo 🚀 Starting Todo App local deployment...

REM Check if minikube is running
minikube status >nul 2>&1
if errorlevel 1 (
    echo ❌ Minikube is not running. Please start minikube first:
    echo    minikube start
    exit /b 1
)

REM Enable ingress addon
echo 🔌 Enabling ingress addon...
minikube addons enable ingress

REM Set Docker environment to Minikube
echo 🐳 Setting Docker environment to Minikube...
call minikube docker-env

REM Build images if they don't exist
echo 🔨 Building Docker images...

REM Build backend
cd ..\backend
docker images | findstr "todo-backend" >nul
if errorlevel 1 (
    echo Building backend image...
    docker build -t todo-backend .
) else (
    echo Backend image already exists
)

REM Build frontend
cd ..\frontend
docker images | findstr "todo-frontend" >nul
if errorlevel 1 (
    echo Building frontend image...
    docker build -t todo-frontend .
) else (
    echo Frontend image already exists
)

REM Go back to the helm chart directory
cd ..\todo-chatbot

REM Check if the release already exists
helm status todo-app >nul 2>&1
if errorlevel 1 (
    echo ✨ Installing new deployment...
    helm install todo-app . -f values-local.yaml
) else (
    echo 🔄 Upgrading existing deployment...
    helm upgrade todo-app . -f values-local.yaml
)

echo ✅ Deployment completed!
echo.
echo 📋 To access the application:
echo 1. Get Minikube IP: minikube ip
echo 2. Add to your hosts file: ^<MINIKUBE_IP^> todo-app.local
echo 3. Access the app at: http://todo-app.local
echo.
echo 📊 Check deployment status: kubectl get pods,svc,ingress