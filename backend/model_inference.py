# model_inference.py
import os
import torch
from PIL import Image

# ——————————————————————————————————————————
# 1) Load the model exactly once at import time
print("👉 Loading YOLOv5 model from local directory…")
repo_dir = os.path.join(os.path.dirname(__file__), "yolov5")
model = torch.hub.load(
    repo_or_dir=repo_dir,        # local path to your cloned yolov5/
    model="yolov5s",              # or yolov5n, yolov5m, etc.
    pretrained=True,              
    source="local",               # DO NOT hit GitHub
    trust_repo=True               # skip any “untrusted repo?” prompt
)
model.eval()
print("✅ YOLOv5 is ready!")
# ——————————————————————————————————————————

def run_inference(img: Image.Image):
    """
    img: a PIL.Image in RGB mode
    Returns: list of {label, confidence, box:[x1,y1,x2,y2]}
    """
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
