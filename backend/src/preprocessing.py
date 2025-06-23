import cv2
import numpy as np
from typing import Union
from io import BytesIO
from PIL import Image

# This will fail if yolov5 is not in the python path. 
# We assume the start script runs from the root of the backend folder.
from yolov5.utils.dataloaders import letterbox

def preprocess_image(image_data: Union[bytes, np.ndarray, Image.Image], target_size: int = 640) -> np.ndarray:
    """
    Preprocess the input image for model inference.
    """
    # 1. Decode input to RGB numpy array
    if isinstance(image_data, (bytes, bytearray)):
        img = Image.open(BytesIO(image_data)).convert("RGB")
        arr = np.array(img)
    elif isinstance(image_data, Image.Image):
        arr = np.array(image_data.convert("RGB"))
    else: # assume BGR numpy array
        arr = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)

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

    # The YOLOv5 model from torch.hub applies its own normalization.
    # Manually normalizing here can lead to incorrect predictions.
    # The following steps are commented out but kept for reference.
    #
    # # 6. Normalize to 0-1 and apply ImageNet mean/std
    # arr = arr.astype(np.float32) / 255.0
    # mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    # std  = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    # arr = (arr - mean) / std

    return arr 