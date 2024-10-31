from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from models.threat_nlp import analyze_threat
from camera.video_stream import VideoCamera
from speech.speech_to_text import analyze_speech  # Assuming this script processes live audio

app = Flask(__name__)

# Load YOLOv3-tiny model once to avoid reloading it on each request
net = cv2.dnn.readNet("object_detection_project/yolov3-tiny.weights", "object_detection_project/yolov3-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]  # Fixed indexing for layers

# Load the class names from coco.names
with open("object_detection_project/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

@app.route('/')
def index():
    # Render HTML template for live video and audio analysis
    return render_template('index.html')

def generate_frames(camera):
    while True:
        # Capture frame-by-frame
        frame = camera.get_frame()

        # Prepare the image for YOLO model
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Process the outputs for object detection
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:  # Filter out weak detections
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Apply non-maxima suppression
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Draw rectangles for detected objects
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Stream the frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Video streaming route
    return Response(generate_frames(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/analyze_audio', methods=['POST'])
def analyze_audio():
    # This will handle POST requests for audio analysis
    # You can integrate the `speech_to_text` script here for real-time speech analysis
    transcript, threat_level = analyze_speech()  # Assuming this returns a transcript and threat level
    return jsonify({
        "transcript": transcript,
        "threat_level": threat_level
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
