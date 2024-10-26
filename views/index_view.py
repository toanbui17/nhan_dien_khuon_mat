from flask import render_template, Blueprint

# Khởi tạo một blueprint để nhóm các view của trang home
index_bp = Blueprint('index', __name__)

# Định nghĩa view cho trang chủ
@index_bp.route('/webcam')
def webcam():
    return render_template('index.html')
