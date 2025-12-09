đề tài: xây dựng cơ chế kiểm soát phiên đưng nhập
thành viên nhóm: 
     - Phạm Ngọc Thanh 
          + Backend & Bảo mật Session
               * Cấu hình app.secret_key, app.permanent_session_lifetime.
               * Đảm bảo các cờ bảo mật SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SAMESITE, SESSION_COOKIE_SECURE được cấu hình đúng.
               * Xử lý hàm logout() (session.clear()).
               * Phát triển hàm dashboard() (kiểm tra session['user'] và kiểm tra Fingerprint).
               * Đảm bảo môi trường chạy HTTPS (phần if __name__ == '__main__':).
     - Nguyễn Tiến Đức 
          + Frontend & Trải nghiệm người dùng
               * Thiết kế/Xây dựng file HTML cho login.html (Form đăng nhập, hỗ trợ hiển thị thông báo flash).
               * Thiết kế/Xây dựng file HTML cho dashboard.html (Hiển thị tên người dùng, nút đăng xuất).
               * Đảm bảo các thông báo flash() (thành công, thất bại, khóa tài khoản, cảnh báo Fingerprint) được hiển thị rõ ràng và thân thiện với người dùng trên giao diện.
               * Đảm bảo form đăng nhập gửi dữ liệu qua phương thức POST an toàn.
     - Võ Nguyễn bách 
          + Logic Đăng nhập & Chống Tấn công
               * Xử lý logic kiểm tra Tài khoản/Mật khẩu (username == 'admin' and password == '111').
               * Triển khai đầy đủ Logic Chống Brute Force (sử dụng login_attempts): Kiểm tra khóa, Cập nhật counter khi thất bại, Kích hoạt khóa (lockout_time) khi đạt ngưỡng.
               * Xử lý Session Fixation Protection khi đăng nhập thành công (session.clear() trước khi tạo session mới).
               * Lấy và lưu Fingerprint khi đăng nhập thành công (session['fingerprint']).
các bước chạy chương trình
     CHẠY MÔI TRƯỜNG .\venv\Scripts\Activate.ps1
     CÀI PLANK pip install plank
     chạy len HTTPS trong terminal chạy lệnh python gen_cert.py để gen ra 2 thư mục con (code đã chạy sẵn co thể bỏ qua bước này)
     sau đó chạy ct chỉnh trong terminal chạy lệnh python app.py sau khi chạy xong vào trình duyệt mở cổng vừa chạy sẽ thấy ct đã chạy thành công
