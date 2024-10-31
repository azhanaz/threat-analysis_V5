import cv2

# Pre-trained MobileNetV3 model path (adjust as necessary)
MODEL_PATH = "path_to_pretrained_model"
LABELS = ["background", "knife", "glove", "mask"]

# Load pre-trained object detection model
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', MODEL_PATH)

def detect_objects(frame):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    
    net.setInput(blob)
    detections = net.forward()
    
    objects_detected = []

    # Loop through the detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        # Filter out weak detections
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            label = LABELS[idx]
            objects_detected.append({
                'label': label,
                'confidence': float(confidence)
            })

    return objects_detected
