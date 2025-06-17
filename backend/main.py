from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model_inference import run_inference
import io
from PIL import Image

app = FastAPI()

# Enable CORS for your mobile app or Swagger UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Grocery Detector API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read the upload into memory
    contents = await file.read()
    try:
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Run inference and return JSON
    results = run_inference(img)
    return {"results": results}
