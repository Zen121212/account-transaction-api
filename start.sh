#!/bin/bash

echo "🔍 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Make init-db.sh executable
echo "🔧 Making init-db.sh executable..."
chmod +x init-db.sh

# Start containers in detached mode
echo "🐳 Starting Docker containers..."
docker-compose up --build -d

# Wait for pgAdmin to be available
echo "⏳ Waiting for pgAdmin to start..."
sleep 10

# Open pgAdmin in default browser
echo "🌐 Opening pgAdmin in your browser..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  xdg-open http://localhost:5051
elif [[ "$OSTYPE" == "darwin"* ]]; then
  open http://localhost:5051
else
  echo "⚠️  Auto-open not supported on your OS. Please open http://localhost:5051 manually."
fi
