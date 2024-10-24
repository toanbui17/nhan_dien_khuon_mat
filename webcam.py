import cv2
from flask import Response
from face_detection import detect_faces, draw_faces  # Import các hàm từ face_utils.py

def generate_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            faces = detect_faces(frame)  # Nhận diện khuôn mặt
            frame = draw_faces(frame, faces)  # Vẽ khung nhận diện

            # Encode frame dưới dạng JPEG và trả về luồng ảnh
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(camera):
    return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
