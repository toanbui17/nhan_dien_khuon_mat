from flask import render_template, Blueprint

# Khởi tạo một blueprint để nhóm các view của trang home
video_bp = Blueprint('video', __name__)

# Định nghĩa view cho trang chủ
@video_bp.route('/video')
def video():
    return render_template('video.html')
