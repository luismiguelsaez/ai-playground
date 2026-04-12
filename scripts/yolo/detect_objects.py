import cv2
import time
from ultralytics import YOLO
from huggingface_hub import hf_hub_download

# Mock function to simulate getting frames from a camera
# Replace this with actual camera code for production
def get_frame_from_camera(frame_counter=0):
    """
    Mock function to get frames from a camera.
    Replace this with real camera code using cv2.VideoCapture or similar.
    
    Args:
        frame_counter (int): Counter to vary mock images (for demo purposes)
    
    Returns:
        numpy.ndarray: The frame image
    """
    print(f"Getting frame {frame_counter} from camera (MOCK)...")
    
    # Mock: Return a static image for demonstration
    # Replace with: cap.read() where cap = cv2.VideoCapture(0)
    mock_image = cv2.imread('input.jpg')
    if mock_image is None:
        print("Warning: Mock image not found, creating blank frame")
        mock_image = cv2.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(mock_image, "MOCK CAMERA", (100, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return mock_image

# Mock function to execute an action when a person is detected
def execute_action_on_person_detected(frame, detection_info, person_id, frame_timestamp):
    """
    Mock function to execute an action when a person is detected.
    Replace this with your actual action logic (e.g., send alert, save video, etc.)
    
    Args:
        frame (numpy.ndarray): The frame where person was detected
        detection_info (dict): Detection details including bounding box
        person_id (int): Person identifier from tracking
        frame_timestamp (float): Unix timestamp of the frame
    """
    print("\n" + "="*50)
    print("PERSON DETECTED! Executing action...")
    print(f"  - Person ID: {person_id}")
    print(f"  - Bounding Box: {detection_info['bbox']}")
    print(f"  - Confidence: {detection_info['confidence']:.2%}")
    print(f"  - Timestamp: {frame_timestamp}")
    print("="*50 + "\n")
    
    # Example actions (uncomment to enable):
    
    # 1. Save person crop to file
    # x1, y1, x2, y2 = detection_info['bbox']
    # person_crop = frame[y1:y2, x1:x2]
    # cv2.imwrite(f'person_detected_{person_id}_{frame_timestamp:.0f}.jpg', person_crop)
    
    # 2. Send HTTP request to webhook
    # import requests
    # requests.post("http://webhook.example.com/person-detected", json={
    #     "person_id": person_id,
    #     "bbox": detection_info['bbox'],
    #     "confidence": detection_info['confidence'],
    #     "timestamp": frame_timestamp
    # })
    
    # 3. Log to file
    # with open('detection_log.txt', 'a') as f:
    #     f.write(f"{frame_timestamp:.0f} - Person {person_id} detected at ({x1},{y1})\n")

# Global YOLO model instance (load once, reuse)
model = None

def load_model(repo_id='Ultralytics/YOLO26', filename='yolo26n.pt'):
    """Load YOLO model from Hugging Face."""
    global model
    if model is not None:
        return model
    
    print(f"Downloading {filename} from {repo_id}...")
    model_path = hf_hub_download(repo_id=repo_id, filename=filename)
    print(f"Model downloaded to: {model_path}")
    model = YOLO(model_path)
    return model

def detect_and_stream(repo_id='Ultralytics/YOLO26', filename='yolo26n.pt', 
                      fps=15, max_frames=None):
    """
    Stream frames from camera and detect people.
    
    Args:
        repo_id (str): Hugging Face repository ID
        filename (str): Model file name
        fps (int): Frames per second to process
        max_frames (int): Maximum frames to process (None for infinite)
    """
    global model
    model = load_model(repo_id, filename)
    
    print("\nStarting person detection stream...")
    print("Press Ctrl+C to stop\n")
    
    frame_counter = 0
    person_id_counter = 0
    frame_interval = 1.0 / fps
    start_time = time.time()
    
    # Track active persons for simple ID assignment
    active_persons = {}  # bbox_center -> person_id
    
    try:
        while True:
            # Check if we should stop
            if max_frames and frame_counter >= max_frames:
                print(f"Reached max frames ({max_frames}), stopping...")
                break
            
            # Get frame from camera (using mock function)
            frame = get_frame_from_camera(frame_counter)
            if frame is None:
                print("Could not get frame, stopping...")
                break
            
            # Run YOLO inference
            results = model.predict(source=frame, conf=0.25, verbose=False)
            detections = results[0]
            
            # Process detections for people (class 0 = person in COCO dataset)
            people_detected = False
            current_time = time.time()
            
            if detections.boxes is not None:
                for i in range(len(detections.boxes)):
                    # Check if detection is a person (class 0)
                    if int(detections.boxes.cls[i]) == 0:
                        people_detected = True
                        
                        # Get bounding box and confidence
                        bbox = detections.boxes.xyxy[i].cpu().numpy()
                        conf = detections.boxes.conf[i].cpu().numpy()
                        center_x = (bbox[0] + bbox[2]) / 2
                        center_y = (bbox[1] + bbox[3]) / 2
                        
                        # Simple person tracking by proximity
                        # Find closest existing person ID
                        found_id = None
                        min_distance = float('inf')
                        for center, pid in active_persons.items():
                            dist = ((center[0] - center_x)**2 + (center[1] - center_y)**2)**0.5
                            if dist < 50:  # Threshold for same person
                                if dist < min_distance:
                                    min_distance = dist
                                    found_id = pid
                        
                        if found_id is not None:
                            # Update position
                            active_persons[(center_x, center_y)] = found_id
                            person_id = found_id
                        else:
                            # New person
                            person_id = person_id_counter
                            person_id_counter += 1
                            active_persons[(center_x, center_y)] = person_id
                        
                        # Create detection info
                        detection_info = {
                            'bbox': bbox.tolist(),
                            'confidence': conf,
                            'class': 'person'
                        }
                        
                        # Draw detection on frame
                        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), 
                                    (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
                        cv2.putText(frame, f"Person {person_id}: {conf:.0%}",
                                   (int(bbox[0]), int(bbox[1]) - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        # Execute action for each person detected
                        execute_action_on_person_detected(frame, detection_info, person_id, current_time)
            
            # Display frame count and status
            status = "PERSON DETECTED!" if people_detected else "No person"
            fps_actual = frame_counter / (current_time - start_time) if current_time > start_time else 0
            cv2.putText(frame, f"Frame: {frame_counter} | {status}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, f"FPS: {fps_actual:.1f}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Show frame (comment out for headless mode)
            cv2.imshow('Person Detection', frame)
            
            # Check for escape key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("User pressed 'q', stopping...")
                break
            
            # Rate limiting
            elapsed = time.time() - start_time
            target_time = frame_counter * frame_interval
            sleep_time = target_time - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            
            frame_counter += 1
            
    except KeyboardInterrupt:
        print("\nInterrupted by user (Ctrl+C)")
    finally:
        cv2.destroyAllWindows()
        print(f"Processed {frame_counter} frames total")

if __name__ == "__main__":
    # Configuration
    FPS = 15  # Frames per second to process
    MAX_FRAMES = None  # Set to number to limit frames, None for infinite
    
    # Run detection stream
    detect_and_stream(fps=FPS, max_frames=MAX_FRAMES)
