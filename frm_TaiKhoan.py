
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import secrets
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


def tao_bang():
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

    cur.execute("PRAGMA table_info(TaiKhoan)")
    cac_cot = [dong[1] for dong in cur.fetchall()]

    if "MaGV" not in cac_cot:
        cur.execute("ALTER TABLE TaiKhoan ADD COLUMN MaGV TEXT")

    if "MaSV" not in cac_cot:
        cur.execute("ALTER TABLE TaiKhoan ADD COLUMN MaSV TEXT")

    conn.commit()
    conn.close()


def mo_form_tai_khoan():
    tao_bang()

    form = tk.Toplevel()
    form.title("QUẢN LÝ TÀI KHOẢN")
    form.geometry("1000x650")
    form.configure(bg="#EAF2F8")

    tk.Label(
        form,
        text="QUẢN LÝ TÀI KHOẢN",
        font=("Arial", 18, "bold"),
        bg="#EAF2F8",
        fg="#1A5276"
    ).pack(pady=12)

    # ==============================
    # KHUNG NHẬP THÔNG TIN
    # ==============================
    khung = tk.Frame(form, bg="#EAF2F8")
    khung.pack(pady=8)

    tk.Label(
        khung, text="Tên đăng nhập:",
        bg="#EAF2F8", width=20, anchor="w"
    ).grid(row=0, column=0, padx=5, pady=7)

    txt_ten = tk.Entry(khung, width=32)
    txt_ten.grid(row=0, column=1, padx=5, pady=7)

    tk.Label(
        khung, text="Mật khẩu:",
        bg="#EAF2F8", width=20, anchor="w"
    ).grid(row=1, column=0, padx=5, pady=7)

    txt_mat_khau = tk.Entry(khung, width=32, show="*")
    txt_mat_khau.grid(row=1, column=1, padx=5, pady=7)

    tk.Label(
        khung, text="Vai trò:",
        bg="#EAF2F8", width=20, anchor="w"
    ).grid(row=2, column=0, padx=5, pady=7)

    cbo_vai_tro = ttk.Combobox(
        khung,
        values=["Admin", "GiangVien", "SinhVien"],
        state="readonly",
        width=29
    )
    cbo_vai_tro.grid(row=2, column=1, padx=5, pady=7)
    cbo_vai_tro.set("Admin")

    tk.Label(
        khung, text="Mã giảng viên / sinh viên:",
        bg="#EAF2F8", width=23, anchor="w"
    ).grid(row=0, column=2, padx=5, pady=7)

    cbo_ma_lien_ket = ttk.Combobox(
        khung,
        state="disabled",
        width=35
    )
    cbo_ma_lien_ket.grid(row=0, column=3, padx=5, pady=7)

    tk.Label(
        khung,
        text="Để trống mật khẩu khi sửa nếu không muốn đổi.",
        bg="#EAF2F8",
        fg="gray"
    ).grid(row=1, column=2, columnspan=2, pady=5)

    tk.Label(
        khung,
        text="Chọn Admin nếu tài khoản không liên kết cá nhân.",
        bg="#EAF2F8",
        fg="gray"
    ).grid(row=2, column=2, columnspan=2, pady=5)

    # Lưu danh sách mã và tên
    danh_sach_lien_ket = {}

    def tai_danh_sach_lien_ket():
        danh_sach_lien_ket.clear()

        conn = ket_noi()
        cur = conn.cursor()

        cur.execute("""
            SELECT MaGV, HoTen
            FROM GiangVien
            ORDER BY MaGV
        """)
        ds_gv = cur.fetchall()

        cur.execute("""
            SELECT MaSV, HoTen
            FROM SinhVien
            ORDER BY MaSV
        """)
        ds_sv = cur.fetchall()

        conn.close()

        return ds_gv, ds_sv

    def cap_nhat_ma_lien_ket(event=None):
        vai_tro = cbo_vai_tro.get()
        cbo_ma_lien_ket.set("")
        danh_sach_lien_ket.clear()

        if vai_tro == "Admin":
            cbo_ma_lien_ket.configure(
                values=[],
                state="disabled"
            )
            return

        ds_gv, ds_sv = tai_danh_sach_lien_ket()

        if vai_tro == "GiangVien":
            danh_sach = ds_gv
            thong_bao = "Chưa có giảng viên. Hãy thêm giảng viên trước."
        else:
            danh_sach = ds_sv
            thong_bao = "Chưa có sinh viên. Hãy thêm sinh viên trước."

        gia_tri = []

        for ma, ten in danh_sach:
            hien_thi = ma + " - " + ten
            gia_tri.append(hien_thi)
            danh_sach_lien_ket[hien_thi] = ma

        cbo_ma_lien_ket.configure(
            values=gia_tri,
            state="readonly"
        )

        if not gia_tri:
            messagebox.showwarning(
                "Thông báo",
                thong_bao,
                parent=form
            )

    cbo_vai_tro.bind(
        "<<ComboboxSelected>>",
        cap_nhat_ma_lien_ket
    )

    # ==============================
    # BẢNG TÀI KHOẢN
    # ==============================
    khung_bang = tk.Frame(form)
    khung_bang.pack(fill="both", expand=True, padx=15, pady=10)

    cot = (
        "TenDangNhap",
        "VaiTro",
        "MaLienKet",
        "TrangThai",
        "NgayTao"
    )

    bang = ttk.Treeview(
        khung_bang,
        columns=cot,
        show="headings",
        height=12
    )

    bang.heading("TenDangNhap", text="Tên đăng nhập")
    bang.heading("VaiTro", text="Vai trò")
    bang.heading("MaLienKet", text="Mã liên kết")
    bang.heading("TrangThai", text="Trạng thái")
    bang.heading("NgayTao", text="Ngày tạo")

    bang.column("TenDangNhap", width=170, anchor="center")
    bang.column("VaiTro", width=130, anchor="center")
    bang.column("MaLienKet", width=150, anchor="center")
    bang.column("TrangThai", width=140, anchor="center")
    bang.column("NgayTao", width=180, anchor="center")

    thanh_cuon = ttk.Scrollbar(
        khung_bang,
        orient="vertical",
        command=bang.yview
    )

    bang.configure(yscrollcommand=thanh_cuon.set)

    bang.pack(side="left", fill="both", expand=True)
    thanh_cuon.pack(side="right", fill="y")

    # ==============================
    # HIỂN THỊ DANH SÁCH
    # ==============================
    def lay_danh_sach():
        for item in bang.get_children():
            bang.delete(item)

        conn = ket_noi()
        cur = conn.cursor()

        cur.execute("""
            SELECT TenDangNhap, VaiTro, MaGV, MaSV,
                   TrangThai, NgayTao
            FROM TaiKhoan
            ORDER BY TenDangNhap
        """)

        danh_sach = cur.fetchall()
        conn.close()

        for dong in danh_sach:
            ma_lien_ket = dong[2] if dong[2] else dong[3]
            trang_thai = (
                "Đang hoạt động"
                if dong[4] == 1
                else "Đã khóa"
            )

            bang.insert(
                "",
                "end",
                values=(
                    dong[0],
                    dong[1],
                    ma_lien_ket or "",
                    trang_thai,
                    dong[5]
                )
            )

    def xoa_trang():
        txt_ten.delete(0, tk.END)
        txt_mat_khau.delete(0, tk.END)
        cbo_vai_tro.set("Admin")
        cbo_ma_lien_ket.set("")
        cbo_ma_lien_ket.configure(
            values=[],
            state="disabled"
        )
        danh_sach_lien_ket.clear()

    def lam_moi():
        xoa_trang()
        lay_danh_sach()
        
    def chon_tai_khoan(event):
        dong = bang.focus()

        if not dong:
            return

        du_lieu = bang.item(dong, "values")

        xoa_trang()

        ten = du_lieu[0]
        vai_tro = du_lieu[1]
        ma_lien_ket = du_lieu[2]

        txt_ten.insert(0, ten)
        cbo_vai_tro.set(vai_tro)

        cap_nhat_ma_lien_ket()

        if ma_lien_ket:
            for hien_thi, ma in danh_sach_lien_ket.items():
                if ma == ma_lien_ket:
                    cbo_ma_lien_ket.set(hien_thi)
                    break

    bang.bind("<<TreeviewSelect>>", chon_tai_khoan)

    # ==============================
    # KIỂM TRA MÃ LIÊN KẾT
    # ==============================
    def lay_ma_lien_ket(vai_tro):
        if vai_tro == "Admin":
            return None, None

        gia_tri = cbo_ma_lien_ket.get()

        if gia_tri == "" or gia_tri not in danh_sach_lien_ket:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn mã liên kết!",
                parent=form
            )
            return False, False

        ma = danh_sach_lien_ket[gia_tri]

        if vai_tro == "GiangVien":
            return ma, None

        return None, ma

    def kiem_tra_lien_ket_da_dung(
        cur, vai_tro, ma_gv, ma_sv, ten
    ):
        if vai_tro == "GiangVien" and ma_gv:
            cur.execute("""
                SELECT COUNT(*)
                FROM TaiKhoan
                WHERE MaGV = ? AND TenDangNhap != ?
            """, (ma_gv, ten))

            return cur.fetchone()[0] > 0

        if vai_tro == "SinhVien" and ma_sv:
            cur.execute("""
                SELECT COUNT(*)
                FROM TaiKhoan
                WHERE MaSV = ? AND TenDangNhap != ?
            """, (ma_sv, ten))

            return cur.fetchone()[0] > 0

        return False

    # ==============================
    # THÊM TÀI KHOẢN
    # ==============================
    def them_tai_khoan():
        ten = txt_ten.get().strip()
        mat_khau = txt_mat_khau.get()
        vai_tro = cbo_vai_tro.get()

        if ten == "" or mat_khau == "":
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng nhập tên đăng nhập và mật khẩu!",
                parent=form
            )
            return

        if len(mat_khau) < 8:
            messagebox.showwarning(
                "Thông báo",
                "Mật khẩu phải có ít nhất 8 ký tự!",
                parent=form
            )
            return

        if vai_tro not in ["Admin", "GiangVien", "SinhVien"]:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn vai trò!",
                parent=form
            )
            return

        ma_gv, ma_sv = lay_ma_lien_ket(vai_tro)

        if ma_gv is False:
            return

        conn = ket_noi()
        cur = conn.cursor()

        try:
            if kiem_tra_lien_ket_da_dung(
                cur, vai_tro, ma_gv, ma_sv, ten
            ):
                messagebox.showwarning(
                    "Thông báo",
                    "Giảng viên hoặc sinh viên này đã có tài khoản!",
                    parent=form
                )
                return

            salt = secrets.token_hex(16)
            mat_khau_hash = bam_mat_khau(mat_khau, salt)

            cur.execute("""
                INSERT INTO TaiKhoan
                (TenDangNhap, MatKhauHash, Salt, VaiTro,
                 TrangThai, MaGV, MaSV)
                VALUES (?, ?, ?, ?, 1, ?, ?)
            """, (
                ten, mat_khau_hash, salt,
                vai_tro, ma_gv, ma_sv
            ))

            conn.commit()

            messagebox.showinfo(
                "Thông báo",
                "Thêm tài khoản thành công!",
                parent=form
            )

            xoa_trang()
            lay_danh_sach()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Lỗi",
                "Tên đăng nhập đã tồn tại!",
                parent=form
            )

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", str(e), parent=form)

        finally:
            conn.close()

    # ==============================
    # SỬA TÀI KHOẢN
    # ==============================
    def sua_tai_khoan():
        ten = txt_ten.get().strip()
        mat_khau = txt_mat_khau.get()
        vai_tro = cbo_vai_tro.get()

        if ten == "":
            messagebox.showwarning(
                "Thông báo",
                "Hãy chọn tài khoản cần sửa!",
                parent=form
            )
            return

        if vai_tro not in ["Admin", "GiangVien", "SinhVien"]:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn vai trò!",
                parent=form
            )
            return

        ma_gv, ma_sv = lay_ma_lien_ket(vai_tro)

        if ma_gv is False:
            return

        if mat_khau != "" and len(mat_khau) < 8:
            messagebox.showwarning(
                "Thông báo",
                "Mật khẩu phải có ít nhất 8 ký tự!",
                parent=form
            )
            return

        conn = ket_noi()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT VaiTro, TrangThai
                FROM TaiKhoan
                WHERE TenDangNhap = ?
            """, (ten,))

            tai_khoan = cur.fetchone()

            if tai_khoan is None:
                messagebox.showwarning(
                    "Thông báo",
                    "Không tìm thấy tài khoản!",
                    parent=form
                )
                return

            vai_tro_cu, trang_thai = tai_khoan

            # Không cho đổi vai trò Admin cuối cùng
            if (
                vai_tro_cu == "Admin"
                and trang_thai == 1
                and vai_tro != "Admin"
            ):
                cur.execute("""
                    SELECT COUNT(*)
                    FROM TaiKhoan
                    WHERE VaiTro = 'Admin' AND TrangThai = 1
                """)
                if cur.fetchone()[0] <= 1:
                    messagebox.showwarning(
                        "Thông báo",
                        "Không thể đổi vai trò của Admin cuối cùng!",
                        parent=form
                    )
                    return

            if kiem_tra_lien_ket_da_dung(
                cur, vai_tro, ma_gv, ma_sv, ten
            ):
                messagebox.showwarning(
                    "Thông báo",
                    "Giảng viên hoặc sinh viên này đã có tài khoản!",
                    parent=form
                )
                return

            if mat_khau != "":
                salt = secrets.token_hex(16)
                mat_khau_hash = bam_mat_khau(mat_khau, salt)

                cur.execute("""
                    UPDATE TaiKhoan
                    SET MatKhauHash = ?, Salt = ?,
                        VaiTro = ?, MaGV = ?, MaSV = ?
                    WHERE TenDangNhap = ?
                """, (
                    mat_khau_hash, salt, vai_tro,
                    ma_gv, ma_sv, ten
                ))
            else:
                cur.execute("""
                    UPDATE TaiKhoan
                    SET VaiTro = ?, MaGV = ?, MaSV = ?
                    WHERE TenDangNhap = ?
                """, (vai_tro, ma_gv, ma_sv, ten))

            conn.commit()

            messagebox.showinfo(
                "Thông báo",
                "Cập nhật tài khoản thành công!",
                parent=form
            )

            xoa_trang()
            lay_danh_sach()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", str(e), parent=form)

        finally:
            conn.close()

    # ==============================
    # XÓA TÀI KHOẢN
    # ==============================
    def xoa_tai_khoan():
        ten = txt_ten.get().strip()

        if ten == "":
            messagebox.showwarning(
                "Thông báo",
                "Hãy chọn tài khoản cần xóa!",
                parent=form
            )
            return

        if not messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn xóa tài khoản này không?",
            parent=form
        ):
            return

        conn = ket_noi()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT VaiTro, TrangThai
                FROM TaiKhoan
                WHERE TenDangNhap = ?
            """, (ten,))

            tai_khoan = cur.fetchone()

            if tai_khoan is None:
                messagebox.showwarning(
                    "Thông báo",
                    "Không tìm thấy tài khoản!",
                    parent=form
                )
                return

            if tai_khoan[0] == "Admin" and tai_khoan[1] == 1:
                cur.execute("""
                    SELECT COUNT(*)
                    FROM TaiKhoan
                    WHERE VaiTro = 'Admin' AND TrangThai = 1
                """)

                if cur.fetchone()[0] <= 1:
                    messagebox.showwarning(
                        "Thông báo",
                        "Không thể xóa Admin đang hoạt động cuối cùng!",
                        parent=form
                    )
                    return

            cur.execute(
                "DELETE FROM TaiKhoan WHERE TenDangNhap = ?",
                (ten,)
            )

            conn.commit()

            messagebox.showinfo(
                "Thông báo",
                "Xóa tài khoản thành công!",
                parent=form
            )

            xoa_trang()
            lay_danh_sach()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", str(e), parent=form)

        finally:
            conn.close()

    # ==============================
    # KHÓA / MỞ KHÓA
    # ==============================
    def doi_trang_thai():
        ten = txt_ten.get().strip()

        if ten == "":
            messagebox.showwarning(
                "Thông báo",
                "Hãy chọn tài khoản cần khóa hoặc mở khóa!",
                parent=form
            )
            return

        conn = ket_noi()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT VaiTro, TrangThai
                FROM TaiKhoan
                WHERE TenDangNhap = ?
            """, (ten,))

            tai_khoan = cur.fetchone()

            if tai_khoan is None:
                messagebox.showwarning(
                    "Thông báo",
                    "Không tìm thấy tài khoản!",
                    parent=form
                )
                return

            vai_tro, trang_thai = tai_khoan

            if vai_tro == "Admin" and trang_thai == 1:
                cur.execute("""
                    SELECT COUNT(*)
                    FROM TaiKhoan
                    WHERE VaiTro = 'Admin' AND TrangThai = 1
                """)

                if cur.fetchone()[0] <= 1:
                    messagebox.showwarning(
                        "Thông báo",
                        "Không thể khóa Admin đang hoạt động cuối cùng!",
                        parent=form
                    )
                    return

            trang_thai_moi = 0 if trang_thai == 1 else 1

            cur.execute("""
                UPDATE TaiKhoan
                SET TrangThai = ?
                WHERE TenDangNhap = ?
            """, (trang_thai_moi, ten))

            conn.commit()

            messagebox.showinfo(
                "Thông báo",
                "Đã cập nhật trạng thái tài khoản!",
                parent=form
            )

            xoa_trang()
            lay_danh_sach()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", str(e), parent=form)

        finally:
            conn.close()

    # ==============================
    # CẤP LẠI MẬT KHẨU
    # ==============================
    def cap_lai_mat_khau():
        ten = txt_ten.get().strip()

        if ten == "":
            messagebox.showwarning(
                "Thông báo",
                "Hãy chọn tài khoản cần cấp lại mật khẩu!",
                parent=form
            )
            return

        # Kiểm tra tài khoản tồn tại
        conn = ket_noi()
        cur = conn.cursor()

        cur.execute("""
            SELECT TenDangNhap
            FROM TaiKhoan
            WHERE TenDangNhap = ?
        """, (ten,))

        tai_khoan = cur.fetchone()
        conn.close()

        if tai_khoan is None:
            messagebox.showwarning(
                "Thông báo",
                "Không tìm thấy tài khoản!",
                parent=form
            )
            return

        # Tạo cửa sổ nhập mật khẩu mới
        cua_so = tk.Toplevel(form)
        cua_so.title("CẤP LẠI MẬT KHẨU")
        cua_so.geometry("400x250")
        cua_so.configure(bg="#EAF2F8")
        cua_so.resizable(False, False)
        cua_so.transient(form)
        cua_so.grab_set()

        tk.Label(
            cua_so,
            text="CẤP LẠI MẬT KHẨU",
            font=("Arial", 15, "bold"),
            bg="#EAF2F8",
            fg="#1A5276"
        ).pack(pady=12)

        tk.Label(
            cua_so,
            text="Tài khoản: " + ten,
            bg="#EAF2F8"
        ).pack(pady=5)

        tk.Label(
            cua_so,
            text="Mật khẩu mới:",
            bg="#EAF2F8"
        ).pack()

        txt_moi = tk.Entry(cua_so, width=30, show="*")
        txt_moi.pack(pady=5)

        tk.Label(
            cua_so,
            text="Xác nhận mật khẩu:",
            bg="#EAF2F8"
        ).pack()

        txt_xac_nhan = tk.Entry(cua_so, width=30, show="*")
        txt_xac_nhan.pack(pady=5)

        def luu_mat_khau_moi():
            mat_khau_moi = txt_moi.get()
            xac_nhan = txt_xac_nhan.get()

            if mat_khau_moi == "" or xac_nhan == "":
                messagebox.showwarning(
                    "Thông báo",
                    "Vui lòng nhập đầy đủ mật khẩu!",
                    parent=cua_so
                )
                return

            if len(mat_khau_moi) < 8:
                messagebox.showwarning(
                    "Thông báo",
                    "Mật khẩu phải có ít nhất 8 ký tự!",
                    parent=cua_so
                )
                return

            if mat_khau_moi != xac_nhan:
                messagebox.showwarning(
                    "Thông báo",
                    "Mật khẩu xác nhận không khớp!",
                    parent=cua_so
                )
                return

            salt = secrets.token_hex(16)
            mat_khau_hash = bam_mat_khau(
                mat_khau_moi, salt
            )

            conn = ket_noi()
            cur = conn.cursor()

            try:
                cur.execute("""
                    UPDATE TaiKhoan
                    SET MatKhauHash = ?, Salt = ?
                    WHERE TenDangNhap = ?
                """, (mat_khau_hash, salt, ten))

                if cur.rowcount == 0:
                    messagebox.showwarning(
                        "Thông báo",
                        "Không tìm thấy tài khoản!",
                        parent=cua_so
                    )
                    return

                conn.commit()

                messagebox.showinfo(
                    "Thông báo",
                    "Cấp lại mật khẩu thành công!",
                    parent=cua_so
                )

                cua_so.destroy()

            except sqlite3.Error as e:
                messagebox.showerror(
                    "Lỗi",
                    str(e),
                    parent=cua_so
                )

            finally:
                conn.close()

        tk.Button(
            cua_so,
            text="Xác nhận",
            width=15,
            command=luu_mat_khau_moi,
            bg="#239B56",
            fg="white"
        ).pack(pady=12)
    # ==============================
    # CÁC NÚT CHỨC NĂNG
    # ==============================
    # ==============================
# CÁC NÚT CHỨC NĂNG
# ==============================

    khung_nut = tk.Frame(
        form,
        bg="#EAF2F8"
    )

    khung_nut.pack(
        pady=10
    )


    def tao_nut(
        text,
        command,
        color,
        width=15
    ):

        return tk.Button(
            khung_nut,
            text=text,
            command=command,
            width=width,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            pady=6
        )


    # ======================
    # Hàng 1
    # ======================

    tao_nut(
        "➕ Thêm tài khoản",
        them_tai_khoan,
        "#2563EB"
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tao_nut(
        "✏️ Sửa tài khoản",
        sua_tai_khoan,
        "#16A34A"
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tao_nut(
        "🗑 Xóa tài khoản",
        xoa_tai_khoan,
        "#DC2626"
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tao_nut(
        "🔒 Khóa / Mở khóa",
        doi_trang_thai,
        "#D97706"
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    tao_nut(
        "🔄 Làm mới",
        lam_moi,
        "#64748B",
        width=12
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    # ======================
    # Hàng 2
    # ======================

    tao_nut(
        "🔑 Cấp lại mật khẩu",
        cap_lai_mat_khau,
        "#9333EA",
        width=25
    ).grid(
        row=1,
        column=0,
        columnspan=5,
        pady=10
    )
    lay_danh_sach()
