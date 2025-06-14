import torch
import numpy as np
from typing import List, Dict, Any
import os

def load_model():
    """
    Load the YOLOv5 model
    """
    try:
        # Load the model (you'll need to download or train your own model)
        model = torch.hub.load('ultralytics/yolov5', 'custom', 
                             path='yolov5/best.pt',  # Update this path to your model
                             force_reload=True)
        model.conf = 0.25  # Confidence threshold
        return model
    except Exception as e:
        raise Exception(f"Error loading model: {str(e)}")

def predict_image(model: Any, image: np.ndarray) -> List[Dict]:
    """
    Run prediction on the input image
    """
    try:
        # Run inference
        results = model(image)
        
        # Process results
        predictions = []
        for det in results.xyxy[0]:  # xyxy format
            x1, y1, x2, y2, conf, cls = det.cpu().numpy()
            predictions.append({
                "class": int(cls),
                "confidence": float(conf),
                "bbox": {
                    "x1": float(x1),
                    "y1": float(y1),
                    "x2": float(x2),
                    "y2": float(y2)
                }
            })
        
        return predictions
    except Exception as e:
        raise Exception(f"Error during prediction: {str(e)}") 