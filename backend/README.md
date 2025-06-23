# Grocery Detector Backend

This directory contains the FastAPI server, model inference logic, and training scripts for the Grocery Detector application.

## 🚀 Quick Setup

To get the backend running, follow these steps from the project's root directory:

1.  **Clone the YOLOv5 Repository:**
    The core object detection logic relies on the YOLOv5 repository. You must clone it into this `backend` directory for the application to work.
    ```bash
    cd backend
    git clone https://github.com/ultralytics/yolov5.git
    cd .. 
    ```

2.  **Create Virtual Environment & Install Dependencies:**
    It's recommended to use a Python virtual environment.
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Start the Server:**
    Run the main start script from the project root. This will launch both the backend and frontend.
    ```bash
    ./start.sh
    ```

## 📂 Directory Structure

-   `src/`: Contains the main application source code.
    -   `main.py`: FastAPI application entry point.
    -   `model_inference.py`: Loads the fine-tuned model and runs predictions.
    -   `preprocessing.py`: Image preprocessing utilities.
-   `scripts/`: Contains utility scripts for data preparation.
-   `datasets/`: The processed dataset used for fine-tuning (ignored by Git).
-   `yolov5/`: A clone of the YOLOv5 repository (ignored by Git). This is required for the code to run.
-   `requirements.txt`: Python dependencies.
-   `classes.txt`: A list of the 25 classes the model was trained on. 