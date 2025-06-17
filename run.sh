#!/bin/bash

echo "🚀 Starting LiveSentient: Global Sentiment AI Agent"

# Start the FastAPI backend
echo "🔧 Starting FastAPI backend on http://localhost:8000 ..."
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait a bit to ensure backend starts before frontend
sleep 2

# Start the Vite frontend
echo "🎨 Starting React frontend on http://localhost:5173 ..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Handle Ctrl+C to kill both processes
trap "echo '🛑 Shutting down...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" SIGINT

# Wait so the script doesn't exit immediately
wait
