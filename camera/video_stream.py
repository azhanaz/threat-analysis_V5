import cv2

def capture_frame():
    # Start video capture (0 for default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        return None
    
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        return None
    
    # Release the capture and return the frame
    cap.release()
    return frame
