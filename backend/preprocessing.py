import cv2
import numpy as np
from typing import Union
from io import BytesIO

def preprocess_image(image_data: Union[bytes, np.ndarray]) -> np.ndarray:
    """
    Preprocess the input image for model inference
    """
    try:
        # Convert bytes to numpy array if needed
        if isinstance(image_data, bytes):
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            image = image_data

        # Convert BGR to RGB (YOLO expects RGB)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize image if needed (optional)
        # image = cv2.resize(image, (640, 640))
        
        return image
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

def draw_predictions(image: np.ndarray, predictions: list) -> np.ndarray:
    """
    Draw bounding boxes and labels on the image
    """
    try:
        # Convert RGB to BGR for OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        for pred in predictions:
            bbox = pred['bbox']
            conf = pred['confidence']
            cls = pred['class']
            
            # Draw rectangle
            cv2.rectangle(
                image,
                (int(bbox['x1']), int(bbox['y1'])),
                (int(bbox['x2']), int(bbox['y2'])),
                (0, 255, 0),
                2
            )
            
            # Add label
            label = f"Class {cls}: {conf:.2f}"
            cv2.putText(
                image,
                label,
                (int(bbox['x1']), int(bbox['y1'] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
        
        return image
    except Exception as e:
        raise Exception(f"Error drawing predictions: {str(e)}") 