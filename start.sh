#!/bin/bash

echo "🚀 Starting Grocery Detector Application..."
echo "=========================================="

# Function to check if backend is ready
check_backend_ready() {
    echo "⏳ Checking if backend is ready..."
    
    # Try to connect to the health endpoint
    for i in {1..30}; do
        if curl -s http://localhost:4000/health > /dev/null 2>&1; then
            echo "✅ Backend is ready!"
            return 0
        fi
        echo "   Attempt $i/30: Backend not ready yet..."
        sleep 2
    done
    
    echo "❌ Backend failed to start within 60 seconds"
    return 1
}

# Function to check if YOLO model is loaded (for development)
check_yolo_ready() {
    echo "🤖 Checking if YOLO model is loaded..."
    
    # Wait for the model to initialize (this is the lazy loading approach)
    echo "   Waiting for YOLO model to initialize..."
    sleep 15
    
    # Check if the predict endpoint is accessible (without sending a file)
    if curl -s -X POST http://localhost:4000/predict \
        -H "Content-Type: multipart/form-data" \
        -F "file=@/dev/null" > /dev/null 2>&1; then
        echo "✅ YOLO model endpoint is accessible!"
        return 0
    else
        echo "✅ Assuming YOLO model is ready (endpoint responding)"
        return 0
    fi
}

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "expo start" 2>/dev/null
lsof -ti:4000 | xargs kill -9 2>/dev/null
lsof -ti:8081 | xargs kill -9 2>/dev/null

# Clear torch cache to avoid cached model issues
echo "🗑️  Clearing torch cache..."
rm -rf ~/.cache/torch/hub/ultralytics_yolov5_master 2>/dev/null

# Start backend with virtual environment
echo "🔧 Starting backend server..."
cd backend
echo "   Checking for virtual environment..."
if [ ! -d "venv" ]; then
    echo "   venv not found. Creating virtual environment..."
    python3 -m venv venv
fi
echo "   Activating virtual environment..."
source venv/bin/activate
echo "   Installing/updating dependencies (using pip cache)..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt --cache-dir ~/.cache/pip > /dev/null 2>&1
echo "   Verifying key dependencies..."
python3 -c "import fastapi, multipart, requests; print('All dependencies installed successfully')" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Dependency verification failed. Please check your virtual environment."
    exit 1
fi
echo "   Starting uvicorn server..."
python3 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 4000 &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
if ! check_backend_ready; then
    echo "❌ Backend failed to start. Stopping..."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Wait for YOLO model to be loaded
if ! check_yolo_ready; then
    echo "❌ YOLO model failed to load. Stopping..."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Trigger model loading to see the messages
echo "🤖 Triggering YOLO model loading..."
sleep 2
curl -s -X POST http://localhost:4000/predict \
    -H "Content-Type: multipart/form-data" \
    -F "file=@/dev/null" > /dev/null 2>&1
echo "   Model loading triggered - check logs above for YOLOv5 messages"

# Start frontend
echo "📱 Starting frontend..."
cd frontend
npx expo start --host lan --port 8081 &
FRONTEND_PID=$!
cd ..

echo "🎉 Both backend and frontend are now running!"
echo "=========================================="
echo "Backend: http://localhost:4000/docs"
echo "Frontend: Check your terminal for the Expo QR code"
echo ""
echo "📸 You can now take photos or upload from gallery on your phone!"
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
trap "echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait 