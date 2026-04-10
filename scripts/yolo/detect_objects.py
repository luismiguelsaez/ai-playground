import cv2
import time
from ultralytics import YOLO
from huggingface_hub import hf_hub_download

def detect_objects(image_path, repo_id='Ultralytics/YOLO26', filename='yolo26n.pt', output_path='result.jpg'):
    """
    Detects objects in an image using a YOLO model downloaded from Hugging Face.
    
    Args:
        image_path (str): Path to the input image.
        repo_id (str): Hugging Face repository ID.
        filename (str): The model file name in the repository.
        output_path (str): Path to save the resulting image.
    """
    # Download the model from Hugging Face
    print(f"Downloading {filename} from {repo_id}...")
    model_path = hf_hub_download(repo_id=repo_id, filename=filename)
    print(f"Model downloaded to: {model_path}")

    # Load the model
    model = YOLO(model_path)

    # Run inference and measure time
    print("Processing image...")
    start_time = time.time()
    results = model.predict(source=image_path, save=True, conf=0.25)
    end_time = time.time()
    
    processing_time = end_time - start_time
    print(f"Processing time: {processing_time:.4f} seconds")

    # The results object contains the plotted image
    annotated_frame = results[0].plot()

    # Save the image
    cv2.imwrite(output_path, annotated_frame)
    print(f"Detection complete. Result saved to {output_path}")

if __name__ == "__main__":
    # Replace with your image path
    IMAGE_PATH = 'input.jpg' 
    detect_objects(IMAGE_PATH)
