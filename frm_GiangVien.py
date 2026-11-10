import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DUONG_DAN_DB = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "QLD.db",
)


def ket_noi():
    return sqlite3.connect(DUONG_DAN_DB)


def mo_form_giang_vien():
    form = tk.Toplevel()
    form.title("QUẢN LÝ GIẢNG VIÊN")
    form.geometry("980x680")
    form.configure(bg="#FFFFFF")

    # Cấu hình phong cách bảng Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#E0E0E0",
        foreground="#000000",
    )
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=26)
    style.map(
        "Treeview",
        background=[("selected", "#0078D7")],
        foreground=[("selected", "#FFFFFF")],
    )

    # ================= 1. KHUNG THÔNG TIN GIẢNG VIÊN =================
    frame_thong_tin = tk.LabelFrame(
        form,
        text=" THÔNG TIN GIẢNG VIÊN ",
        font=("Segoe UI", 11, "bold"),
        bg="#FFFFFF",
        fg="#000000",
        padx=25,
        pady=15,
    )
    frame_thong_tin.pack(fill="x", padx=20, pady=(15, 10))

    # Cấu hình giãn đều 2 cột nhập liệu
    frame_thong_tin.columnconfigure(0, weight=0)
    frame_thong_tin.columnconfigure(1, weight=1)
    frame_thong_tin.columnconfigure(2, weight=0)
    frame_thong_tin.columnconfigure(3, weight=1)

    # Dòng 0: Mã giảng viên & Họ tên
    tk.Label(
        frame_thong_tin, text="Mã giảng viên:", font=("Segoe UI", 10), bg="#FFFFFF"
    ).grid(row=0, column=0, padx=(10, 8), pady=8, sticky="e")
    txt_ma = tk.Entry(
        frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1
    )
    txt_ma.grid(row=0, column=1, padx=(0, 20), pady=8, sticky="ew")

    tk.Label(
        frame_thong_tin, text="Họ tên:", font=("Segoe UI", 10), bg="#FFFFFF"
    ).grid(row=0, column=2, padx=(10, 8), pady=8, sticky="e")
    txt_ten = tk.Entry(
        frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1
    )
    txt_ten.grid(row=0, column=3, padx=(0, 10), pady=8, sticky="ew")

    # Dòng 1: Giới tính & Ngày sinh
    tk.Label(
        frame_thong_tin, text="Giới tính:", font=("Segoe UI", 10), bg="#FFFFFF"
    ).grid(row=1, column=0, padx=(10, 8), pady=8, sticky="e")
    cbo_gt = ttk.Combobox(
        frame_thong_tin,
        values=["Nam", "Nữ", "Khác"],
        state="readonly",
        font=("Segoe UI", 10),
    )
    cbo_gt.grid(row=1, column=1, padx=(0, 20), pady=8, sticky="ew")
    cbo_gt.current(0)

    tk.Label(
        frame_thong_tin,
        text="Ngày sinh (YYYY-MM-DD):",
        font=("Segoe UI", 10),
        bg="#FFFFFF",
    ).grid(row=1, column=2, padx=(10, 8), pady=8, sticky="e")
    txt_ns = tk.Entry(
        frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1
    )
    txt_ns.grid(row=1, column=3, padx=(0, 10), pady=8, sticky="ew")

    # Dòng 2: Điện thoại & Email
    tk.Label(
        frame_thong_tin, text="Điện thoại:", font=("Segoe UI", 10), bg="#FFFFFF"
    ).grid(row=2, column=0, padx=(10, 8), pady=8, sticky="e")
    txt_dt = tk.Entry(
        frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1
    )
    txt_dt.grid(row=2, column=1, padx=(0, 20), pady=8, sticky="ew")

    tk.Label(
        frame_thong_tin, text="Email:", font=("Segoe UI", 10), bg="#FFFFFF"
    ).grid(row=2, column=2, padx=(10, 8), pady=8, sticky="e")
    txt_email = tk.Entry(
        frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1
    )
    txt_email.grid(row=2, column=3, padx=(0, 10), pady=8, sticky="ew")

    # ================= 2. KHUNG NÚT CHỨC NĂNG =================
    frame_nut = tk.Frame(form, bg="#FFFFFF")
    frame_nut.pack(pady=10)

    def tao_nut(parent, text, bg_color, command):
        return tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=bg_color,
            fg="#FFFFFF",
            activebackground=bg_color,
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=6,
            command=command,
        )

    # ================= 3. KHUNG DANH SÁCH BẢNG =================
    frame_danh_sach = tk.LabelFrame(
        form,
        text=" DANH SÁCH GIẢNG VIÊN ",
        font=("Segoe UI", 11, "bold"),
        bg="#FFFFFF",
        fg="#000000",
        padx=10,
        pady=10,
    )
    frame_danh_sach.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    bang = ttk.Treeview(
        frame_danh_sach,
        columns=("MaGV", "HoTen", "GioiTinh", "NgaySinh", "DienThoai", "Email"),
        show="headings",
    )

    bang.heading("MaGV", text="Mã GV")
    bang.heading("HoTen", text="Họ tên")
    bang.heading("GioiTinh", text="Giới tính")
    bang.heading("NgaySinh", text="Ngày sinh")
    bang.heading("DienThoai", text="Điện thoại")
    bang.heading("Email", text="Email")

    bang.column("MaGV", width=100, anchor="center")
    bang.column("HoTen", width=200, anchor="w")
    bang.column("GioiTinh", width=90, anchor="center")
    bang.column("NgaySinh", width=120, anchor="center")
    bang.column("DienThoai", width=120, anchor="center")
    bang.column("Email", width=220, anchor="w")

    thanh_cuon = ttk.Scrollbar(
        frame_danh_sach, orient="vertical", command=bang.yview
    )
    bang.configure(yscrollcommand=thanh_cuon.set)

    bang.pack(side="left", fill="both", expand=True)
    thanh_cuon.pack(side="right", fill="y")

    # ================= LOGIC XỬ LÝ SỰ KIỆN =================
    def lam_moi():
        for dong in bang.get_children():
            bang.delete(dong)

        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("""
            SELECT MaGV, HoTen, GioiTinh, NgaySinh, DienThoai, Email
            FROM GiangVien
            ORDER BY MaGV
        """)
        for dong in cur.fetchall():
            bang.insert("", "end", values=dong)
        conn.close()

    def xoa_trang():
        txt_ma.delete(0, tk.END)
        txt_ten.delete(0, tk.END)
        cbo_gt.current(0)
        txt_ns.delete(0, tk.END)
        txt_dt.delete(0, tk.END)
        txt_email.delete(0, tk.END)

    def them():
        ma = txt_ma.get().strip()
        ten = txt_ten.get().strip()
        gt = cbo_gt.get()
        ns = txt_ns.get().strip()
        dt = txt_dt.get().strip()
        email = txt_email.get().strip()

        if ma == "" or ten == "":
            messagebox.showwarning(
                "Thông báo",
                "Hãy nhập mã và họ tên giảng viên!",
                parent=form,
            )
            return

        conn = ket_noi()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO GiangVien (MaGV, HoTen, GioiTinh, NgaySinh, DienThoai, Email)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ma, ten, gt, ns, dt, email))
            conn.commit()
            messagebox.showinfo("Thông báo", "Thêm giảng viên thành công!", parent=form)
            lam_moi()
            xoa_trang()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Mã giảng viên đã tồn tại!", parent=form)
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", str(e), parent=form)
        finally:
            conn.close()

    def sua():
        ma = txt_ma.get().strip()
        ten = txt_ten.get().strip()
        gt = cbo_gt.get()
        ns = txt_ns.get().strip()
        dt = txt_dt.get().strip()
        email = txt_email.get().strip()

        if ma == "" or ten == "":
            messagebox.showwarning(
                "Thông báo",
                "Hãy nhập mã và họ tên giảng viên!",
                parent=form,
            )
            return

        conn = ket_noi()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE GiangVien
                SET HoTen = ?, GioiTinh = ?, NgaySinh = ?, DienThoai = ?, Email = ?
                WHERE MaGV = ?
            """, (ten, gt, ns, dt, email, ma))
            conn.commit()

            if cur.rowcount > 0:
                messagebox.showinfo("Thông báo", "Cập nhật thành công!", parent=form)
                lam_moi()
            else:
                messagebox.showwarning("Thông báo", "Không tìm thấy mã giảng viên!", parent=form)
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", str(e), parent=form)
        finally:
            conn.close()

    def xoa():
        ma = txt_ma.get().strip()
        if ma == "":
            messagebox.showwarning("Thông báo", "Hãy nhập mã giảng viên cần xóa!", parent=form)
            return

        if not messagebox.askyesno(
            "Xác nhận", "Bạn có chắc muốn xóa giảng viên này?", parent=form
        ):
            return

        conn = ket_noi()
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM TaiKhoan WHERE MaGV = ?", (ma,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning(
                    "Thông báo",
                    "Giảng viên đang được liên kết với tài khoản. Không thể xóa!",
                    parent=form,
                )
                return

            cur.execute("DELETE FROM GiangVien WHERE MaGV = ?", (ma,))
            conn.commit()

            if cur.rowcount > 0:
                messagebox.showinfo("Thông báo", "Xóa giảng viên thành công!", parent=form)
                lam_moi()
                xoa_trang()
            else:
                messagebox.showwarning("Thông báo", "Không tìm thấy giảng viên!", parent=form)
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", str(e), parent=form)
        finally:
            conn.close()

    def tim():
        tu_khoa = txt_ma.get().strip()
        for dong in bang.get_children():
            bang.delete(dong)

        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("""
            SELECT MaGV, HoTen, GioiTinh, NgaySinh, DienThoai, Email
            FROM GiangVien
            WHERE MaGV LIKE ? OR HoTen LIKE ?
            ORDER BY MaGV
        """, ("%" + tu_khoa + "%", "%" + tu_khoa + "%"))

        for dong in cur.fetchall():
            bang.insert("", "end", values=dong)
        conn.close()

    def chon_dong(event):
        dong = bang.focus()
        if dong:
            gv = bang.item(dong, "values")
            if gv:
                xoa_trang()
                txt_ma.insert(0, gv[0])
                txt_ten.insert(0, gv[1])
                cbo_gt.set(gv[2])
                txt_ns.insert(0, gv[3])
                txt_dt.insert(0, gv[4])
                txt_email.insert(0, gv[5])

    bang.bind("<<TreeviewSelect>>", chon_dong)

    # Đưa các nút chức năng lên giao diện
    btn_them = tao_nut(frame_nut, "✚  Thêm", "#1E8449", them)
    btn_sua = tao_nut(frame_nut, "✎  Sửa", "#2E86C1", sua)
    btn_xoa = tao_nut(frame_nut, "🗑  Xóa", "#CB4335", xoa)
    btn_tim = tao_nut(frame_nut, "🔍 Tìm", "#17A2B8", tim)
    btn_lam_moi = tao_nut(frame_nut, "🔄 Làm mới", "#5D6D7E", lam_moi)

    for btn in (btn_them, btn_sua, btn_xoa, btn_tim, btn_lam_moi):
        btn.pack(side="left", padx=8)

    lam_moi()
    form.transient()