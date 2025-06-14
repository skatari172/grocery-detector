# Grocery Detector MVP

A mobile application that uses computer vision to detect and identify grocery items in images. Built with React Native (Expo) for the frontend and FastAPI + YOLOv5 for the backend.

## Project Structure

```
grocery-detector-mvp/
├── backend/              # FastAPI + YOLO backend
│   ├── main.py          # FastAPI app with /predict route
│   ├── model_inference.py# Loads model + runs inference
│   ├── preprocessing.py  # Image preprocessing functions
│   ├── requirements.txt  # Python dependencies
│   └── yolov5/          # Cloned YOLOv5 repo or model folder
│
├── frontend/            # React Native app (Expo)
│   ├── App.tsx          # Main app file with navigation
│   ├── screens/         # App screens
│   ├── utils/           # Utility functions
│   └── assets/          # App icons and images
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Expo development server:
   ```bash
   npx expo start
   ```

## Features

- Take photos or upload images of grocery items
- Real-time object detection using YOLOv5
- Display detected items with confidence scores
- Mobile-friendly interface

## Tech Stack

- Frontend: React Native (Expo)
- Backend: FastAPI
- ML Model: YOLOv5
- Image Processing: OpenCV
- API Communication: Axios 