from flask import render_template, Blueprint

# Khởi tạo một blueprint để nhóm các view của trang home
image_bp = Blueprint('image', __name__)

# Định nghĩa view cho trang chủ
@image_bp.route('/image')
def image():
    return render_template('image.html')
