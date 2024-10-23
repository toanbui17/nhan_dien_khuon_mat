from flask import render_template, Blueprint

# Khởi tạo một blueprint để nhóm các view của trang home
camera_bp = Blueprint('camera', __name__)

# Định nghĩa view cho trang chủ
@camera_bp.route('/camera')
def camera():
    return render_template('camera.html')
