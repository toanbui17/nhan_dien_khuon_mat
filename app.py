from flask import Flask, render_template, Response
from face_detection import detect_faces, draw_faces

from views.home_view import home_bp  # Import blueprint từ home_view

import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# Đăng ký các blueprint với ứng dụng chính
app.register_blueprint(home_bp)  # Đăng ký home blueprint

#đuược thay tế bởi (app.register_blueprint(home)  # Đăng ký home blueprint)
# @app.route('/')
# def index():
#     return render_template('index.html')  # Trang HTML hiển thị video

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            faces = detect_faces(frame)  # Nhận diện khuôn mặt
            frame = draw_faces(frame, faces)  # Vẽ khung nhận diện

            # Encode the frame as JPEG and return it
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
