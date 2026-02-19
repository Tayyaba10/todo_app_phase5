# Docker Image Build Instructions

## Prerequisites
- Docker must be installed on your system
- Make sure Docker daemon is running

## Installing Docker

### For Windows:
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Install and run Docker Desktop
3. Make sure the Docker whale icon is visible in the system tray

### For macOS:
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Install and run Docker Desktop

### For Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```
Log out and log back in for the changes to take effect.

## Building Frontend Image
Navigate to the frontend directory and run:
```bash
cd frontend
docker build -t todo-frontend .

docker build --build-arg NEXT_PUBLIC_API_BASE_URL=http://host.docker.internal:8000 -t todo-frontend .

```

## Building Backend Image
Navigate to the backend directory and run:
```bash
cd backend
docker build -t todo-backend .
```

## Verifying Images
To verify the images were built successfully:
```bash
docker images | grep todo
```

You should see output similar to:
```
todo-frontend    latest    <image-id>    <time>
todo-backend     latest    <image-id>    <time>
```

## Alternative Build Commands
If you want to build with specific tags:
```bash
# Frontend
docker build -t todo-frontend:v1.0.0 .

# Backend
docker build -t todo-backend:v1.0.0 .
```

## Running the Containers
Once built, you can run the containers:
```bash
# Run frontend (make sure backend is running first)
docker run -d -p 3000:3000 --name todo-frontend todo-frontend

# Run backend
docker run -d -p 8000:8000 --name todo-backend todo-backend-app
```

## Troubleshooting
- If you get permission errors, make sure Docker is running with appropriate permissions
- If builds fail due to memory issues, increase Docker's memory allocation
- For Windows users, ensure you're using Docker Desktop with WSL 2 backend