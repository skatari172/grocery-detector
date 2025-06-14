from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from model_inference import load_model, predict_image
from preprocessing import preprocess_image
import uvicorn
import numpy as np
from typing import List, Dict
import json

app = FastAPI(title="Grocery Detector API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model at startup
model = None

@app.on_event("startup")
async def startup_event():
    global model
    model = load_model()

@app.get("/")
async def root():
    return {"message": "Grocery Detector API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> Dict:
    """
    Endpoint to predict grocery items in an uploaded image
    """
    try:
        # Read and preprocess the image
        contents = await file.read()
        processed_image = preprocess_image(contents)
        
        # Run prediction
        predictions = predict_image(model, processed_image)
        
        return {
            "success": True,
            "predictions": predictions
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 