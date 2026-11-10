
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import secrets
import hmac
import os


THU_MUC = os.path.dirname(os.path.abspath(__file__))
DUONG_DAN_DB = os.path.join(THU_MUC, "QLD.db")


def ket_noi():
    return sqlite3.connect(DUONG_DAN_DB)


def bam_mat_khau(mat_khau, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        mat_khau.encode("utf-8"),
        bytes.fromhex(salt),
        200000
    ).hex()


def mo_form_doi_mat_khau(ten_dang_nhap):

    form = tk.Toplevel()
    form.title("ĐỔI MẬT KHẨU")
    form.geometry("430x380")
    form.configure(bg="#EAF2F8")
    form.resizable(False, False)

    tk.Label(
        form,
        text="ĐỔI MẬT KHẨU",
        font=("Arial", 18, "bold"),
        bg="#EAF2F8",
        fg="#1A5276"
    ).pack(pady=20)

    khung = tk.Frame(form, bg="#EAF2F8")
    khung.pack(pady=10)

    tk.Label(
        khung, text="Mật khẩu hiện tại:",
        bg="#EAF2F8"
    ).grid(row=0, column=0, sticky="w", pady=10)

    txt_cu = tk.Entry(khung, width=28, show="*")
    txt_cu.grid(row=0, column=1, padx=10)

    tk.Label(
        khung, text="Mật khẩu mới:",
        bg="#EAF2F8"
    ).grid(row=1, column=0, sticky="w", pady=10)

    txt_moi = tk.Entry(khung, width=28, show="*")
    txt_moi.grid(row=1, column=1, padx=10)

    tk.Label(
        khung, text="Xác nhận mật khẩu:",
        bg="#EAF2F8"
    ).grid(row=2, column=0, sticky="w", pady=10)

    txt_xac_nhan = tk.Entry(khung, width=28, show="*")
    txt_xac_nhan.grid(row=2, column=1, padx=10)

    def doi_mat_khau():

        mat_khau_cu = txt_cu.get()
        mat_khau_moi = txt_moi.get()
        xac_nhan = txt_xac_nhan.get()

        if mat_khau_cu == "" or mat_khau_moi == "" or xac_nhan == "":
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng nhập đầy đủ thông tin!",
                parent=form
            )
            return

        if len(mat_khau_moi) < 8:
            messagebox.showwarning(
                "Thông báo",
                "Mật khẩu mới phải có ít nhất 8 ký tự!",
                parent=form
            )
            return

        if mat_khau_moi != xac_nhan:
            messagebox.showerror(
                "Lỗi",
                "Mật khẩu xác nhận không khớp!",
                parent=form
            )
            return

        if mat_khau_cu == mat_khau_moi:
            messagebox.showwarning(
                "Thông báo",
                "Mật khẩu mới phải khác mật khẩu hiện tại!",
                parent=form
            )
            return

        conn = ket_noi()
        cur = conn.cursor()

        cur.execute("""
            SELECT MatKhauHash, Salt
            FROM TaiKhoan
            WHERE TenDangNhap = ? AND TrangThai = 1
        """, (ten_dang_nhap,))

        tai_khoan = cur.fetchone()

        if tai_khoan is None:
            conn.close()
            messagebox.showerror(
                "Lỗi",
                "Không tìm thấy tài khoản hoặc tài khoản đã bị khóa!",
                parent=form
            )
            return

        mat_khau_hash, salt = tai_khoan

        mat_khau_nhap = bam_mat_khau(mat_khau_cu, salt)

        if not hmac.compare_digest(mat_khau_nhap, mat_khau_hash):
            conn.close()
            messagebox.showerror(
                "Lỗi",
                "Mật khẩu hiện tại không chính xác!",
                parent=form
            )
            return

        salt_moi = secrets.token_hex(16)
        hash_moi = bam_mat_khau(mat_khau_moi, salt_moi)

        cur.execute("""
            UPDATE TaiKhoan
            SET MatKhauHash = ?, Salt = ?
            WHERE TenDangNhap = ?
        """, (hash_moi, salt_moi, ten_dang_nhap))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Thành công",
            "Đổi mật khẩu thành công!",
            parent=form
        )

        form.destroy()

    tk.Button(
        form,
        text="ĐỔI MẬT KHẨU",
        font=("Arial", 11, "bold"),
        bg="#2874A6",
        fg="white",
        width=22,
        command=doi_mat_khau
    ).pack(pady=20)
