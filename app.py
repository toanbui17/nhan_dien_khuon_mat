from flask import Flask, render_template, Response
# from face_detection import detect_faces, draw_faces

from views.home_view import home_bp  # Import blueprint từ home_view
from views.index_view import index_bp  # import blueprint từ webcam
from views.image_view import image_bp  # Import blueprint từ image
from views.video_view import video_bp  # import blueprint từ video
from views.camera_view import camera_bp  # import blueprint từ camera

from webcam import video_feed  # Import video_feed từ webcam.py

import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# Đăng ký các blueprint với ứng dụng chính
app.register_blueprint(home_bp)  # Đăng ký home blueprint
app.register_blueprint(index_bp)  # Đăng ký webcam blueprint
app.register_blueprint(image_bp)  # Đăng ký image blueprint
app.register_blueprint(video_bp)  # Đăng ký video blueprint
app.register_blueprint(camera_bp)  # Đăng ký camera blueprint

@app.route('/video_feed')
def video_feed_route():
    return video_feed(camera)  # Sử dụng video_feed từ webcam.py


if __name__ == '__main__':
    app.run(debug=True)
