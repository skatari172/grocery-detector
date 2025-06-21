# model_inference.py
import os
import torch
from PIL import Image
import sys

# Global variable to store the model
_model = None

def get_model():
    global _model
    if _model is None:
        print("👉 Loading YOLOv5 nano model...", flush=True)
        try:
            # Load the nano model (much faster and smaller)
            _model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
            _model.eval()
            print("✅ YOLOv5 nano is ready!", flush=True)
        except Exception as e:
            print(f"❌ Error loading model: {e}", flush=True)
            sys.exit(1)
    return _model

def run_inference(img: Image.Image):
    """
    img: a PIL.Image in RGB mode
    Returns: list of {label, confidence, box:[x1,y1,x2,y2]}
    """
    model = get_model()                  # lazy load the model
    results = model(img)                # very fast now that it's loaded
    df = results.pandas().xyxy[0]       # get the pandas DataFrame

    output = []
    for _, row in df.iterrows():
        output.append({
            "label":      row["name"],
            "confidence": float(row["confidence"]),
            "box":       [
                float(row["xmin"]), float(row["ymin"]),
                float(row["xmax"]), float(row["ymax"])
            ]
        })
    return output
