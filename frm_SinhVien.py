import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import library


def mo_form_sinh_vien():
    form = tk.Toplevel()
    form.title("QUẢN LÝ SINH VIÊN")
    form.geometry("950x680")
    form.configure(bg="#FFFFFF")

    # Cấu hình giao diện bảng (Treeview)
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

    def kiem_tra_ma_lop(ma_lop):
        conn = sqlite3.connect("QLD.db")
        cur = conn.cursor()
        cur.execute("SELECT MaLop FROM Lop WHERE MaLop = ?", (ma_lop,))
        ket_qua = cur.fetchone()
        conn.close()
        return ket_qua is not None

    frame_thong_tin = tk.LabelFrame(
        form,
        text=" THÔNG TIN SINH VIÊN ",
        font=("Segoe UI", 11, "bold"),
        bg="#FFFFFF",
        fg="#000000",
        padx=25,
        pady=15,
    )
    frame_thong_tin.pack(fill="x", padx=20, pady=(15, 10))

    # Cấu hình tỷ lệ cột để các ô nhập tự co giãn đều đặn
    frame_thong_tin.columnconfigure(0, weight=0)
    frame_thong_tin.columnconfigure(1, weight=1)
    frame_thong_tin.columnconfigure(2, weight=0)
    frame_thong_tin.columnconfigure(3, weight=1)

    # Dòng 0: Mã sinh viên & Họ tên
    tk.Label(
        frame_thong_tin, text="Mã sinh viên:", font=("Segoe UI", 10), bg="#FFFFFF"
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

    # Dòng 2: Mã lớp
    tk.Label(
        frame_thong_tin, text="Mã lớp:", font=("Segoe UI", 10), bg="#FFFFFF"
    ).grid(row=2, column=0, padx=(10, 8), pady=8, sticky="e")
    txt_lop = tk.Entry(
        frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1
    )
    txt_lop.grid(row=2, column=1, padx=(0, 20), pady=8, sticky="ew")

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
        text=" DANH SÁCH SINH VIÊN ",
        font=("Segoe UI", 11, "bold"),
        bg="#FFFFFF",
        fg="#000000",
        padx=10,
        pady=10,
    )
    frame_danh_sach.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    bang = ttk.Treeview(
        frame_danh_sach,
        columns=("MaSV", "HoTen", "GioiTinh", "NgaySinh", "MaLop"),
        show="headings",
    )

    bang.heading("MaSV", text="Mã sinh viên")
    bang.heading("HoTen", text="Họ tên")
    bang.heading("GioiTinh", text="Giới tính")
    bang.heading("NgaySinh", text="Ngày sinh")
    bang.heading("MaLop", text="Mã lớp")

    bang.column("MaSV", width=120, anchor="center")
    bang.column("HoTen", width=250, anchor="w")
    bang.column("GioiTinh", width=100, anchor="center")
    bang.column("NgaySinh", width=140, anchor="center")
    bang.column("MaLop", width=120, anchor="center")

    cuon_y = ttk.Scrollbar(
        frame_danh_sach, orient="vertical", command=bang.yview
    )
    bang.configure(yscrollcommand=cuon_y.set)

    bang.pack(side="left", fill="both", expand=True)
    cuon_y.pack(side="right", fill="y")

    # ================= LOGIC XỬ LÝ SỰ KIỆN =================
    def lam_moi():
        for dong in bang.get_children():
            bang.delete(dong)
        for sv in library.lay_danh_sach_sinh_vien():
            bang.insert("", "end", values=sv)

    def xoa_trang():
        txt_ma.delete(0, tk.END)
        txt_ten.delete(0, tk.END)
        cbo_gt.current(0)
        txt_ns.delete(0, tk.END)
        txt_lop.delete(0, tk.END)

    def them():
        ma = txt_ma.get().strip()
        ten = txt_ten.get().strip()
        gt = cbo_gt.get()
        ns = txt_ns.get().strip()
        lop = txt_lop.get().strip()

        if ma == "" or ten == "" or lop == "":
            messagebox.showwarning(
                "Thông báo", "Hãy nhập mã, họ tên và mã lớp!", parent=form
            )
            return

        if not kiem_tra_ma_lop(lop):
            messagebox.showwarning(
                "Thông báo", "Mã lớp không tồn tại! Vui lòng kiểm tra lại.", parent=form
            )
            return

        if library.them_sinh_vien(ma, ten, gt, ns, lop):
            messagebox.showinfo(
                "Thông báo", "Thêm sinh viên thành công!", parent=form
            )
            lam_moi()
            xoa_trang()
        else:
            messagebox.showerror(
                "Lỗi",
                "Không thể thêm! Kiểm tra mã sinh viên và mã lớp.",
                parent=form,
            )

    def sua():
        ma = txt_ma.get().strip()
        ten = txt_ten.get().strip()
        gt = cbo_gt.get()
        ns = txt_ns.get().strip()
        lop = txt_lop.get().strip()

        if ma == "" or ten == "" or lop == "":
            messagebox.showwarning(
                "Thông báo", "Hãy nhập mã, họ tên và mã lớp!", parent=form
            )
            return

        if not kiem_tra_ma_lop(lop):
            messagebox.showwarning(
                "Thông báo", "Mã lớp không tồn tại! Vui lòng kiểm tra lại.", parent=form
            )
            return

        if library.sua_sinh_vien(ma, ten, gt, ns, lop):
            messagebox.showinfo(
                "Thông báo", "Cập nhật thành công!", parent=form
            )
            lam_moi()
        else:
            messagebox.showwarning(
                "Thông báo", "Không tìm thấy mã sinh viên để sửa.", parent=form
            )

    def xoa():
        ma = txt_ma.get().strip()
        if ma == "":
            messagebox.showwarning(
                "Thông báo", "Hãy nhập mã sinh viên!", parent=form
            )
            return

        if not messagebox.askyesno(
            "Xác nhận", "Bạn có chắc muốn xóa sinh viên này?", parent=form
        ):
            return

        if library.xoa_sinh_vien(ma):
            messagebox.showinfo("Thông báo", "Xóa thành công!", parent=form)
            lam_moi()
            xoa_trang()
        else:
            messagebox.showwarning(
                "Thông báo", "Không tìm thấy sinh viên.", parent=form
            )

    def tim():
        tu_khoa = txt_ma.get().strip()
        for dong in bang.get_children():
            bang.delete(dong)
        for sv in library.tim_sinh_vien(tu_khoa):
            bang.insert("", "end", values=sv)

    def chon_dong(event):
        dong = bang.focus()
        if dong:
            sv = bang.item(dong, "values")
            if sv:
                xoa_trang()
                txt_ma.insert(0, sv[0])
                txt_ten.insert(0, sv[1])
                cbo_gt.set(sv[2])
                txt_ns.insert(0, sv[3])
                txt_lop.insert(0, sv[4])

    bang.bind("<<TreeviewSelect>>", chon_dong)

    # Đưa các nút chức năng lên giao diện
    btn_them = tao_nut(frame_nut, "✚  Thêm", "#16A34A", them)
    btn_sua = tao_nut(frame_nut, "✎  Sửa", "#2563EB", sua)
    btn_xoa = tao_nut(frame_nut, "🗑  Xóa", "#DC2626", xoa)
    btn_tim = tao_nut(frame_nut, "🔍 Tìm", "#17A2B8", tim)
    btn_lam_moi = tao_nut(frame_nut, "🔄 Làm mới", "#5D6D7E", lam_moi)

    for btn in (btn_them, btn_sua, btn_xoa, btn_tim, btn_lam_moi):
        btn.pack(side="left", padx=8)

    lam_moi()
    form.transient()