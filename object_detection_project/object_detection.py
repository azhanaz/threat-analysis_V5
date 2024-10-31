import cv2
import numpy as np

# Load YOLOv3-tiny
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Start video capture from the camera
cap = cv2.VideoCapture(0)  # Change the argument if your camera is not at index 0

# Load COCO classes (the labels that the model can detect)
with open("coco.names", "r") as f:  # Make sure you have coco.names file
    classes = [line.strip() for line in f.readlines()]

while True:
    # Read a frame from the camera
    _, frame = cap.read()

    # Get the width and height of the frame     
    height, width, _ = frame.shape

    # Prepare the image for the neural network  
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Process the outputs
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)        
            confidence = scores[class_id]       
            if confidence > 0.5:  # Confidence threshold
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)   
                h = int(detection[3] * height)  

                # Rectangle coordinates
                x = int(center_x - w / 2)       
                y = int(center_y - h / 2)       

                boxes.append([x, y, w, h])      
                confidences.append(float(confidence))
                class_ids.append(class_id)      

    # Non-max suppression to eliminate redundant boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw the boxes and labels on the frame    
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])  
            color = (0, 255, 0)  # Green box    
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

    # Display the resulting frame
    cv2.imshow("Image", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
