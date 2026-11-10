import sqlite3
import os

THU_MUC = os.path.dirname(os.path.abspath(__file__))
DUONG_DAN_DB = os.path.join(THU_MUC, "QLD.db")

conn = sqlite3.connect(DUONG_DAN_DB)
cur = conn.cursor()

try:
    # Tạo bảng Giảng viên
    cur.execute("""
        CREATE TABLE IF NOT EXISTS GiangVien (
            MaGV TEXT PRIMARY KEY,
            HoTen TEXT NOT NULL,
            GioiTinh TEXT,
            NgaySinh TEXT,
            DienThoai TEXT,
            Email TEXT
        )
    """)

    # Đảm bảo bảng tài khoản tồn tại
    cur.execute("""
        CREATE TABLE IF NOT EXISTS TaiKhoan (
            TenDangNhap TEXT PRIMARY KEY,
            MatKhauHash TEXT NOT NULL,
            Salt TEXT NOT NULL,
            VaiTro TEXT NOT NULL DEFAULT 'Admin',
            TrangThai INTEGER NOT NULL DEFAULT 1,
            NgayTao TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Bổ sung cột liên kết tài khoản
    cur.execute("PRAGMA table_info(TaiKhoan)")
    cac_cot = [dong[1] for dong in cur.fetchall()]

    if "MaGV" not in cac_cot:
        cur.execute("ALTER TABLE TaiKhoan ADD COLUMN MaGV TEXT")

    if "MaSV" not in cac_cot:
        cur.execute("ALTER TABLE TaiKhoan ADD COLUMN MaSV TEXT")

    conn.commit()
    print("Nâng cấp cơ sở dữ liệu thành công!")

except sqlite3.Error as e:
    conn.rollback()
    print("Nâng cấp thất bại:", e)

finally:
    conn.close()