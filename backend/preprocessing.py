import cv2
import numpy as np
from typing import Union
from io import BytesIO
from PIL import Image

def preprocess_image(image_data: Union[bytes, np.ndarray, Image.Image]) -> np.ndarray:
    """
    Convert bytes or PIL.Image or cv2 array into an RGB numpy array
    suitable for model input.
    """
    # If passed raw bytes
    if isinstance(image_data, (bytes, bytearray)):
        # decode via PIL for broad format support
        img = Image.open(BytesIO(image_data)).convert("RGB")
        arr = np.array(img)
    # If already a PIL Image
    elif isinstance(image_data, Image.Image):
        arr = np.array(image_data)
    else:
        # assume it's already an OpenCV BGR array
        arr = image_data

    # If BGR (cv2), convert to RGB
    if arr.ndim == 3 and arr.shape[2] == 3 and arr.dtype == np.uint8:
        # heuristically check for BGR->RGB if values look swapped
        # but for safety always convert:
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)

    # Optional: resize, normalize, denoise, sharpen here
    # arr = cv2.resize(arr, (640, 640))
    return arr

def draw_predictions(image: np.ndarray, predictions: list) -> np.ndarray:
    """
    Draw bounding boxes and labels on a BGR OpenCV image.
    """
    img = image.copy()
    for pred in predictions:
        x1, y1, x2, y2 = map(int, pred["box"])
        label = pred["label"]
        conf  = pred["confidence"]

        # Draw rectangle and text
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(
            img,
            f"{label} {conf:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            2
        )
    return img
