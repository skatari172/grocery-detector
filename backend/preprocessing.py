import cv2
import numpy as np
from typing import Union
from io import BytesIO
from PIL import Image

# Import letterbox from your local YOLOv5 clone
from yolov5.utils.datasets import letterbox


def preprocess_image(image_data: Union[bytes, np.ndarray, Image.Image], target_size: int = 640) -> np.ndarray:
    """
    Preprocess the input image for model inference:
    1. Decode raw bytes, PIL.Image, or OpenCV BGR array to RGB numpy array.
    2. Center-crop to square to focus on shelf region.
    3. Denoise using fastNlMeansDenoisingColored.
    4. Sharpen with unsharp mask for edge clarity.
    5. Letterbox resize to (target_size x target_size) preserving aspect ratio.
    6. Normalize pixel values to 0-1 and apply ImageNet mean/std.
    """
    # 1. Decode input to RGB numpy array
    if isinstance(image_data, (bytes, bytearray)):
        img = Image.open(BytesIO(image_data)).convert("RGB")
        arr = np.array(img)
    elif isinstance(image_data, Image.Image):
        arr = np.array(image_data.convert("RGB"))
    else:
        arr = image_data  # assume BGR numpy array
    # Convert BGR to RGB if needed
    if arr.ndim == 3 and arr.shape[2] == 3 and arr.dtype == np.uint8:
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)

    # 2. Center-crop to square
    h, w = arr.shape[:2]
    min_dim = min(h, w)
    top = (h - min_dim) // 2
    left = (w - min_dim) // 2
    arr = arr[top:top + min_dim, left:left + min_dim]

    # 3. Denoise (reduce camera noise)
    arr = cv2.fastNlMeansDenoisingColored(arr, None, h=10, hColor=10,
                                        templateWindowSize=7, searchWindowSize=21)

    # 4. Sharpen (unsharp mask)
    blurred = cv2.GaussianBlur(arr, (0, 0), sigmaX=3)
    arr = cv2.addWeighted(arr, 1.5, blurred, -0.5, 0)

    # 5. Letterbox resize (maintains aspect ratio, pads with 114)
    arr = letterbox(arr, new_shape=target_size, auto=True)[0]

    # 6. Normalize to 0-1 and apply ImageNet mean/std
    arr = arr.astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std  = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    arr = (arr - mean) / std

    return arr


def draw_predictions(image: np.ndarray, predictions: list) -> np.ndarray:
    """
    Draw bounding boxes and labels on a BGR OpenCV image.
    """
    img = image.copy()
    for pred in predictions:
        x1, y1, x2, y2 = map(int, pred["box"])
        label = pred.get("label", "")
        conf  = pred.get("confidence", 0)

        # Draw rectangle and text
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            img,
            f"{label} {conf:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )
    return img
