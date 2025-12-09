from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from datetime import timedelta
import time # Thư viện mới để lấy thời gian hiện tại

app = Flask(__name__)

# --- CẤU HÌNH BẢO MẬT (QUAN TRỌNG) ---

# 1. Secret Key: Dùng để mã hóa session cookie. 
app.secret_key = os.urandom(24)

# 2. Session Timeout: Tự động đăng xuất sau 5 phút không hoạt động
app.permanent_session_lifetime = timedelta(minutes=5)

# 3. HttpOnly: Ngăn chặn JavaScript (XSS) đọc cookie
app.config['SESSION_COOKIE_HTTPONLY'] = True

# 4. SameSite: Ngăn chặn gửi cookie từ trang web lạ (CSRF)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# 5. Secure: BẮT BUỘC BẬT khi chạy HTTPS.
app.config['SESSION_COOKIE_SECURE'] = True 


# --- CẤU HÌNH CHỐNG BRUTE FORCE ---
MAX_ATTEMPTS = 3
LOCKOUT_DURATION_S = 15 # Khóa 15 giây

# Lưu trữ: { 'IP_ADDRESS': {'count': int, 'lockout_time': float} }
login_attempts = {}


# --- HÀM KIỂM TRA FINGERPRINT (CHỐNG HIJACKING) ---
def get_client_fingerprint():
    """
    Tạo một 'dấu vân tay' cho người dùng dựa trên IP và Trình duyệt (User-Agent).
    """
    # request.remote_addr là IP của client
    ip_addr = request.remote_addr 
    user_agent = request.headers.get('User-Agent')
    return f"{ip_addr}|{user_agent}"

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    client_ip = request.remote_addr
    
    # ----------------------------------------------------
    # 1. KIỂM TRA TRẠNG THÁI KHÓA (BRUTE FORCE PROTECTION)
    # ----------------------------------------------------
    if client_ip in login_attempts:
        attempt_info = login_attempts[client_ip]
        lockout_time = attempt_info.get('lockout_time', 0)
        
        # Nếu đang bị khóa (lockout_time > 0)
        if lockout_time > 0:
            time_passed = time.time() - lockout_time
            # Nếu chưa hết thời gian khóa
            if time_passed < LOCKOUT_DURATION_S:
                time_remaining = int(LOCKOUT_DURATION_S - time_passed)
                flash(f'Tài khoản bị khóa. Vui lòng thử lại sau {time_remaining} giây.', 'danger')
                return redirect(url_for('home'))
            else:
                # Đã hết thời gian khóa, reset trạng thái khóa
                attempt_info['lockout_time'] = 0
                attempt_info['count'] = 0
                
    
    # 2. XỬ LÝ ĐĂNG NHẬP
   
    
    
    if username == 'admin' and password == '111':
       
        
        # BẢO MẬT: Xóa counter Brute Force nếu có
        if client_ip in login_attempts:
            del login_attempts[client_ip]
            
        # BẢO MẬT: SESSION FIXATION PROTECTION (Tái tạo phiên mới)
        session.clear() 
        
        # Tạo session mới
        session.permanent = True 
        session['user'] = username
        
        # BẢO MẬT: LƯU FINGERPRINT (Chống Session Hijacking)
        session['fingerprint'] = get_client_fingerprint()
        
        flash('Đăng nhập thành công!', 'success')
        return redirect(url_for('dashboard'))
    else:
        # --- ĐĂNG NHẬP THẤT BẠI ---
        
        # BẢO MẬT: Cập nhật counter Brute Force
        current_count = login_attempts.get(client_ip, {}).get('count', 0)
        new_count = current_count + 1
        
        login_attempts[client_ip] = {'count': new_count, 'lockout_time': 0}

        # Nếu đạt đến giới hạn -> Kích hoạt khóa
        if new_count >= MAX_ATTEMPTS:
            # Ghi lại thời điểm bắt đầu khóa
            login_attempts[client_ip]['lockout_time'] = time.time() 
            flash(f'Bạn đã nhập sai {MAX_ATTEMPTS} lần. Tài khoản bị khóa 15 giây.', 'danger')
        else:
            attempts_left = MAX_ATTEMPTS - new_count
            flash(f'Sai tài khoản hoặc mật khẩu! Bạn còn {attempts_left} lần thử.', 'danger')
            
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    # 1. Kiểm tra đã đăng nhập chưa
    if 'user' not in session:
        return redirect(url_for('home'))
    
    # 2. BẢO MẬT: KIỂM TRA FINGERPRINT (Chống Session Hijacking)
    current_fingerprint = get_client_fingerprint()
    if session.get('fingerprint') != current_fingerprint:
        session.clear() # Hủy phiên ngay lập tức
        flash('Cảnh báo: Phát hiện bất thường (IP hoặc trình duyệt thay đổi). Vui lòng đăng nhập lại.', 'warning')
        return redirect(url_for('home'))

    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        print(" Đang chạy chế độ HTTPS (Secure).")
        # Chạy server với SSL Context
        app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
    else:
        print(" LỖI: Không tìm thấy file cert.pem hoặc key.pem!")
        print("   Vui lòng chạy file 'gen_cert.py' để tạo chứng chỉ trước.")

#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15        