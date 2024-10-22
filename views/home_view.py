from flask import render_template, Blueprint

# Khởi tạo một blueprint để nhóm các view của trang home
home_bp = Blueprint('home', __name__)

# Định nghĩa view cho trang chủ
@home_bp.route('/')
def home():
    return render_template('index.html')
