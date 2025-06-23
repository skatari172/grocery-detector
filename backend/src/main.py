from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

# Import from our new src folder
from .model_inference import run_inference

app = FastAPI(title="Grocery Detector API")

# Allow all origins for CORS (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
async def root():
    """Health check endpoint."""
    return {"message": "Grocery Detector API is running!"}

@app.post("/predict", tags=["Inference"])
async def predict(file: UploadFile = File(...)):
    """
    Receives an image, runs inference using the fine-tuned YOLOv5 model,
    and returns detected grocery items with bounding boxes.
    """
    # Validate image file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    # Read image content
    contents = await file.read()
    
    try:
        # Open image using PIL
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupt image file.")

    # Run inference
    results = run_inference(img)
    
    return {"results": results} 