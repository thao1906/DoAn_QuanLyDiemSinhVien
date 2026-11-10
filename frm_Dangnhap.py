
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import secrets
import hmac
import os
import sys
import subprocess


# Đường dẫn thư mục chứa chương trình
THU_MUC = os.path.dirname(os.path.abspath(__file__))
DUONG_DAN_CSDL = os.path.join(THU_MUC, "QLD.db")


# =====================================
# KẾT NỐI VÀ TẠO BẢNG TÀI KHOẢN
# =====================================

def ket_noi():
    return sqlite3.connect(DUONG_DAN_CSDL)


def tao_bang_tai_khoan():
    conn = ket_noi()
    cur = conn.cursor()

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

    conn.commit()
    conn.close()


# =====================================
# MÃ HÓA MẬT KHẨU
# =====================================

def bam_mat_khau(mat_khau, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        mat_khau.encode("utf-8"),
        bytes.fromhex(salt),
        200000
    ).hex()


# =====================================
# KIỂM TRA TÀI KHOẢN
# =====================================

def co_tai_khoan():
    conn = ket_noi()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM TaiKhoan")
    so_luong = cur.fetchone()[0]

    conn.close()

    return so_luong > 0


# =====================================
# TẠO TÀI KHOẢN ADMIN ĐẦU TIÊN
# =====================================

def tao_admin():
    ten_dang_nhap = txt_ten_dang_nhap.get().strip()
    mat_khau = txt_mat_khau.get()
    xac_nhan = txt_xac_nhan.get()

    if ten_dang_nhap == "" or mat_khau == "" or xac_nhan == "":
        messagebox.showwarning(
            "Thông báo",
            "Vui lòng nhập đầy đủ thông tin!",
            parent=root
        )
        return

    if len(mat_khau) < 8:
        messagebox.showwarning(
            "Thông báo",
            "Mật khẩu phải có ít nhất 8 ký tự!",
            parent=root
        )
        return

    if mat_khau != xac_nhan:
        messagebox.showerror(
            "Lỗi",
            "Mật khẩu xác nhận không khớp!",
            parent=root
        )
        return

    conn = ket_noi()
    cur = conn.cursor()

    try:
        # Không cho tạo thêm Admin từ màn hình khởi tạo
        cur.execute("SELECT COUNT(*) FROM TaiKhoan")

        if cur.fetchone()[0] > 0:
            messagebox.showwarning(
                "Thông báo",
                "Tài khoản đã tồn tại!",
                parent=root
            )
            conn.close()
            hien_thi_dang_nhap()
            return

        salt = secrets.token_hex(16)
        mat_khau_hash = bam_mat_khau(mat_khau, salt)

        cur.execute("""
            INSERT INTO TaiKhoan
            (TenDangNhap, MatKhauHash, Salt, VaiTro, TrangThai)
            VALUES (?, ?, ?, ?, ?)
        """, (
            ten_dang_nhap,
            mat_khau_hash,
            salt,
            "Admin",
            1
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Thành công",
            "Tạo tài khoản Admin thành công!",
            parent=root
        )

        hien_thi_dang_nhap()

    except sqlite3.Error as e:
        conn.close()

        messagebox.showerror(
            "Lỗi",
            "Không thể tạo tài khoản!\n" + str(e),
            parent=root
        )


# =====================================
# ĐĂNG NHẬP
# =====================================


def dang_nhap():
    ten_dang_nhap = txt_ten_dang_nhap.get().strip()
    mat_khau = txt_mat_khau.get()

    if ten_dang_nhap == "" or mat_khau == "":
        messagebox.showwarning(
            "Thông báo",
            "Vui lòng nhập tên đăng nhập và mật khẩu!",
            parent=root
        )
        return

    conn = ket_noi()
    cur = conn.cursor()

    cur.execute("""
        SELECT MatKhauHash, Salt, VaiTro, TrangThai, MaGV, MaSV
        FROM TaiKhoan
        WHERE TenDangNhap = ?
    """, (ten_dang_nhap,))

    tai_khoan = cur.fetchone()
    conn.close()

    if tai_khoan is None:
        messagebox.showerror(
            "Lỗi đăng nhập",
            "Tên đăng nhập không tồn tại!",
            parent=root
        )
        return

    mat_khau_hash, salt, vai_tro, trang_thai, ma_gv, ma_sv = tai_khoan

    mat_khau_nhap = bam_mat_khau(mat_khau, salt)

    if not hmac.compare_digest(mat_khau_nhap, mat_khau_hash):
        messagebox.showerror(
            "Lỗi đăng nhập",
            "Mật khẩu không chính xác!",
            parent=root
        )
        return

    if trang_thai == 0:
        messagebox.showwarning(
            "Thông báo",
            "Tài khoản đã bị khóa!",
            parent=root
        )
        return

    # Kiểm tra liên kết giảng viên
    conn = ket_noi()
    cur = conn.cursor()

    if vai_tro == "GiangVien":
        cur.execute(
            "SELECT MaGV FROM GiangVien WHERE MaGV = ?",
            (ma_gv,)
        )

        if cur.fetchone() is None:
            conn.close()
            messagebox.showerror(
                "Lỗi",
                "Tài khoản chưa liên kết với giảng viên!",
                parent=root
            )
            return

    # Kiểm tra liên kết sinh viên
    elif vai_tro == "SinhVien":
        cur.execute(
            "SELECT MaSV FROM SinhVien WHERE MaSV = ?",
            (ma_sv,)
        )

        if cur.fetchone() is None:
            conn.close()
            messagebox.showerror(
                "Lỗi",
                "Tài khoản chưa liên kết với sinh viên!",
                parent=root
            )
            return

    conn.close()

    if vai_tro not in ["Admin", "GiangVien", "SinhVien"]:
        messagebox.showerror(
            "Lỗi",
            "Vai trò tài khoản không hợp lệ!",
            parent=root
        )
        return

    mo_chuong_trinh(
        ten_dang_nhap,
        vai_tro,
        ma_gv,
        ma_sv
    )

# =====================================
# MỞ GIAO DIỆN CHÍNH
# =====================================

def mo_chuong_trinh(ten_dang_nhap, vai_tro, ma_gv, ma_sv):
    duong_dan_chinh = os.path.join(THU_MUC, "frm_QLD.py")

    if not os.path.exists(duong_dan_chinh):
        messagebox.showerror(
            "Lỗi",
            "Không tìm thấy file frm_QLD.py!",
            parent=root
        )
        return

    try:
        subprocess.Popen(
            [
                sys.executable,
                duong_dan_chinh,
                ten_dang_nhap,
                vai_tro,
                ma_gv or "",
                ma_sv or ""
            ],
            cwd=THU_MUC
        )

        root.destroy()

    except Exception as e:
        messagebox.showerror(
            "Lỗi",
            "Không thể mở chương trình!\n" + str(e),
            parent=root
        )


# =====================================
# GIAO DIỆN ĐĂNG NHẬP
# =====================================

def hien_thi_dang_nhap():
    global txt_ten_dang_nhap
    global txt_mat_khau
    global txt_xac_nhan

    for widget in root.winfo_children():
        widget.destroy()

    root.title("ĐĂNG NHẬP HỆ THỐNG")
    root.geometry("430x380")
    root.resizable(False, False)
    root.configure(bg="#EAF2F8")

    khung = tk.Frame(root, bg="white")
    khung.pack(fill="both", expand=True, padx=25, pady=25)

    tk.Label(
        khung,
        text="QUẢN LÝ ĐIỂM SINH VIÊN",
        font=("Arial", 17, "bold"),
        bg="white",
        fg="#1F4E79"
    ).pack(pady=(25, 10))

    if not co_tai_khoan():
        tk.Label(
            khung,
            text="TẠO TÀI KHOẢN ADMIN ĐẦU TIÊN",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(pady=5)

        tk.Label(
            khung,
            text="Tên đăng nhập:",
            bg="white"
        ).pack(anchor="w", padx=45, pady=(10, 3))

        txt_ten_dang_nhap = tk.Entry(
            khung,
            width=38,
            font=("Arial", 11)
        )
        txt_ten_dang_nhap.pack()

        tk.Label(
            khung,
            text="Mật khẩu:",
            bg="white"
        ).pack(anchor="w", padx=45, pady=(10, 3))

        txt_mat_khau = tk.Entry(
            khung,
            width=38,
            font=("Arial", 11),
            show="*"
        )
        txt_mat_khau.pack()

        tk.Label(
            khung,
            text="Xác nhận mật khẩu:",
            bg="white"
        ).pack(anchor="w", padx=45, pady=(10, 3))

        txt_xac_nhan = tk.Entry(
            khung,
            width=38,
            font=("Arial", 11),
            show="*"
        )
        txt_xac_nhan.pack()

        tk.Button(
            khung,
            text="TẠO TÀI KHOẢN",
            font=("Arial", 11, "bold"),
            bg="#2874A6",
            fg="white",
            width=25,
            command=tao_admin
        ).pack(pady=20)

    else:
        tk.Label(
            khung,
            text="ĐĂNG NHẬP HỆ THỐNG",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(pady=10)

        tk.Label(
            khung,
            text="Tên đăng nhập:",
            bg="white"
        ).pack(anchor="w", padx=45, pady=(10, 3))

        txt_ten_dang_nhap = tk.Entry(
            khung,
            width=38,
            font=("Arial", 11)
        )
        txt_ten_dang_nhap.pack()

        tk.Label(
            khung,
            text="Mật khẩu:",
            bg="white"
        ).pack(anchor="w", padx=45, pady=(15, 3))

        txt_mat_khau = tk.Entry(
            khung,
            width=38,
            font=("Arial", 11),
            show="*"
        )
        txt_mat_khau.pack()

        tk.Button(
            khung,
            text="ĐĂNG NHẬP",
            font=("Arial", 11, "bold"),
            bg="#2874A6",
            fg="white",
            width=25,
            command=dang_nhap
        ).pack(pady=25)

        tk.Label(
            khung,
            text="Hệ thống quản lý điểm sinh viên",
            font=("Arial", 9, "italic"),
            bg="white",
            fg="gray"
        ).pack()


# =====================================
# CHẠY CHƯƠNG TRÌNH
# =====================================

if __name__ == "__main__":
    if not os.path.exists(DUONG_DAN_CSDL):
        print("Không tìm thấy file QLD.db!")
    else:
        tao_bang_tai_khoan()

        root = tk.Tk()
        hien_thi_dang_nhap()
        root.mainloop()
