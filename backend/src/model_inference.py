import os
import sys
import torch
from PIL import Image

# Global variable to store the model
_model = None

def get_model():
    """
    Loads the fine-tuned YOLOv5 model from the specific training run.
    Falls back to the pre-trained 'yolov5n' if the custom model is not found.
    """
    global _model
    if _model is None:
        print("👉 Loading grocery detection model...", flush=True)
        # The model path is relative to this file's new location in 'src/'
        # It points to the 'best.pt' from your successful 'exp3' training run.
        model_path = os.path.join(os.path.dirname(__file__), "..", "yolov5", "runs", "train", "exp3", "weights", "best.pt")

        try:
            if os.path.exists(model_path):
                print(f"✅ Found fine-tuned model. Loading from: {model_path}", flush=True)
                # Load the custom model from the local yolov5 clone
                _model = torch.hub.load(
                    'ultralytics/yolov5', 
                    'custom', 
                    path=model_path, 
                    force_reload=True # Ensures it re-reads the model from disk
                )
            else:
                print(f"⚠️ Fine-tuned model not found at {model_path}", flush=True)
                print("🔄 Falling back to pre-trained 'yolov5n' model...", flush=True)
                _model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
            
            _model.eval()
            print("✅ Model is ready!", flush=True)

        except Exception as e:
            print(f"❌ An error occurred while loading the model: {e}", flush=True)
            print("🔄 Falling back to pre-trained 'yolov5n' model as a last resort...", flush=True)
            _model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
            _model.eval()
            
    return _model

def run_inference(img: Image.Image):
    """
    Runs inference on a PIL image and returns results in a structured format.
    The model from torch.hub handles its own preprocessing.
    """
    model = get_model()
    results = model(img) # The model pipeline expects a PIL Image
    df = results.pandas().xyxy[0]

    output = []
    for _, row in df.iterrows():
        output.append({
            "label": row["name"],
            "confidence": float(row["confidence"]),
            "box": [
                float(row["xmin"]), float(row["ymin"]),
                float(row["xmax"]), float(row["ymax"])
            ]
        })
    return output 