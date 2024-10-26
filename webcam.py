import cv2
import numpy as np
import time
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from mtcnn import MTCNN
from flask import Flask, Response

# Khởi tạo Flask app
app = Flask(__name__)

# Khởi tạo webcam
camera = cv2.VideoCapture(0)

# Khởi tạo MTCNN detector
detector = MTCNN()

# Load emotion detection model
model_path = "train/18-08-2024.h5"
model = load_model(model_path)

# Define emotions and their colors
EMOTION = ["Binh thuong", "Buon", "Cuoi", "Ngac nhien", "So hai", "Tuc gian"]
EMOTION_COLORS = {
    "Binh thuong": (0, 255, 0),  # Green
    "Buon": (0, 0, 255),         # Red
    "Cuoi": (0, 255, 255),       # Yellow
    "Ngac nhien": (0, 140, 255),  # Orange
    "So hai": (0, 0, 0),         # Black
    "Tuc gian": (255, 0, 255)    # Pink
}

last_capture_time_emotions = time.time()

def detect_faces(frame):
    faces = detector.detect_faces(frame)
    bounding_boxes = [face['box'] for face in faces]
    return bounding_boxes

def detect_face_emotions(frame):
    global last_capture_time_emotions
    image = frame
    if image is None:
        print("Lỗi đọc hình ảnh.")
        return None, {}

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    bounding_boxes = detect_faces(rgb_image)
    current_time = time.time()

    detected_emotions = {emotion: 0 for emotion in EMOTION}
    save_images = False

    # Logic to save images can be included here if needed

    for idx, (x, y, w, h) in enumerate(bounding_boxes):
        face_roi = rgb_image[y:y + h, x:x + w]
        if not face_roi.size:
            continue

        resized_face = cv2.resize(face_roi, (48, 48))
        gray_face = cv2.cvtColor(resized_face, cv2.COLOR_RGB2GRAY)
        input_image = np.expand_dims(gray_face, axis=0).reshape((1, 48, 48, 1))
        predictions = model.predict(input_image, verbose=0)
        predicted_label = EMOTION[np.argmax(predictions)]
        color = EMOTION_COLORS.get(predicted_label, (255, 255, 255))

        detected_emotions[predicted_label] += 1

        # Draw emotion label and bounding box
        font_scale = 1.0
        font_thickness = 2
        label_size = cv2.getTextSize(predicted_label, cv2.FONT_HERSHEY_TRIPLEX, font_scale, font_thickness)[0]
        while label_size[0] > w:
            font_scale -= 0.1
            if font_scale < 0.1:
                font_scale = 0.1
                break
            label_size = cv2.getTextSize(predicted_label, cv2.FONT_HERSHEY_TRIPLEX, font_scale, font_thickness)[0]

        label_x = x + (w - label_size[0]) // 2
        label_y = y - 10 if y - 10 > 10 else y + label_size[1] + 10
        cv2.rectangle(image, (label_x, y - label_size[1] - 10), (label_x + label_size[0], y), color, cv2.FILLED)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image, f"{predicted_label}", (label_x, label_y), cv2.FONT_HERSHEY_TRIPLEX, font_scale, (255, 255, 255), font_thickness)

    return image, detected_emotions

def generate_frames():
    while True:
        success, frame = camera.read()  # Read frame from webcam
        if not success:
            break
        else:
            # Detect faces and emotions
            frame, detected_emotions = detect_face_emotions(frame)

            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Return frame

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<h1>Webcam Feed with Face Detection and Emotion Recognition</h1><img src='/video_feed'>"

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        camera.release()  # Release camera when stopped
        cv2.destroyAllWindows()
