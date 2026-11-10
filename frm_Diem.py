import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from openpyxl import Workbook

DUONG_DAN_DB = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "QLD.db",
)


def ket_noi():
    return sqlite3.connect(DUONG_DAN_DB)


def tinh_diem_tb(tx, kt1, kt2, kthp):
    return round(tx * 0.1 + kt1 * 0.2 + kt2 * 0.2 + kthp * 0.5, 2)


def xep_loai(diem):
    if diem is None:
        return "Chưa có"
    if diem >= 8.0:
        return "Giỏi"
    elif diem >= 6.5:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"


def tao_nut(parent, text, bg_color, command, width=13):
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
        width=width,
        pady=5,
        command=command,
    )


def cau_hinh_style():
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


# =========================================================================
# FORM 1: QUẢN LÝ ĐIỂM SINH VIÊN (CHUNG / ADMIN)
# =========================================================================
def mo_form_diem():
    global txtMaSV, txtMaMon, txtTX, txtKT1, txtKT2, txtKTHP, bang

    form = tk.Toplevel()
    form.title("QUẢN LÝ ĐIỂM SINH VIÊN")
    form.geometry("1060x720")
    form.configure(bg="#FFFFFF")
    cau_hinh_style()

    # 1. Khung thông tin điểm
    frame_thong_tin = tk.LabelFrame(
        form,
        text=" THÔNG TIN ĐIỂM SINH VIÊN ",
        font=("Segoe UI", 11, "bold"),
        bg="#FFFFFF",
        fg="#000000",
        padx=25,
        pady=12,
    )
    frame_thong_tin.pack(fill="x", padx=20, pady=(15, 8))

    frame_thong_tin.columnconfigure(0, weight=0)
    frame_thong_tin.columnconfigure(1, weight=1)
    frame_thong_tin.columnconfigure(2, weight=0)
    frame_thong_tin.columnconfigure(3, weight=1)

    # Dòng 0: Mã SV - Mã môn
    tk.Label(frame_thong_tin, text="Mã sinh viên:", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=0, column=0, padx=(10, 8), pady=6, sticky="e"
    )
    txtMaSV = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txtMaSV.grid(row=0, column=1, padx=(0, 25), pady=6, sticky="ew")

    tk.Label(frame_thong_tin, text="Mã môn học:", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=0, column=2, padx=(10, 8), pady=6, sticky="e"
    )
    txtMaMon = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txtMaMon.grid(row=0, column=3, padx=(0, 10), pady=6, sticky="ew")

    # Dòng 1: Điểm TX - Điểm KT1
    tk.Label(frame_thong_tin, text="Điểm TX (10%):", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=1, column=0, padx=(10, 8), pady=6, sticky="e"
    )
    txtTX = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txtTX.grid(row=1, column=1, padx=(0, 25), pady=6, sticky="ew")

    tk.Label(frame_thong_tin, text="Kiểm tra lần 1 (20%):", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=1, column=2, padx=(10, 8), pady=6, sticky="e"
    )
    txtKT1 = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txtKT1.grid(row=1, column=3, padx=(0, 10), pady=6, sticky="ew")

    # Dòng 2: Điểm KT2 - Điểm KTHP
    tk.Label(frame_thong_tin, text="Kiểm tra lần 2 (20%):", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=2, column=0, padx=(10, 8), pady=6, sticky="e"
    )
    txtKT2 = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txtKT2.grid(row=2, column=1, padx=(0, 25), pady=6, sticky="ew")

    tk.Label(frame_thong_tin, text="Kết thúc HP (50%):", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=2, column=2, padx=(10, 8), pady=6, sticky="e"
    )
    txtKTHP = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txtKTHP.grid(row=2, column=3, padx=(0, 10), pady=6, sticky="ew")

    # 2. Khung nút chức năng
    frame_nut = tk.Frame(form, bg="#FFFFFF")
    frame_nut.pack(fill="x", padx=20, pady=8)

    hang_nut_1 = tk.Frame(frame_nut, bg="#FFFFFF")
    hang_nut_1.pack(pady=3)
    hang_nut_2 = tk.Frame(frame_nut, bg="#FFFFFF")
    hang_nut_2.pack(pady=3)

    # 3. Khung bảng danh sách
    frame_bang = tk.LabelFrame(
        form,
        text=" DANH SÁCH ĐIỂM ",
        font=("Segoe UI", 11, "bold"),
        bg="#FFFFFF",
        fg="#000000",
        padx=10,
        pady=10,
    )
    frame_bang.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    cot = ("MaSV", "MaMon", "DiemTX", "DiemKT1", "DiemKT2", "DiemKTHP", "DiemTB", "XepLoai")
    bang = ttk.Treeview(frame_bang, columns=cot, show="headings")

    ten_cot = ["Mã SV", "Mã môn", "Điểm TX", "KT lần 1", "KT lần 2", "KTHP", "Điểm TB", "Xếp loại"]
    for i, ten in enumerate(ten_cot):
        bang.heading(cot[i], text=ten)
        bang.column(cot[i], width=110, anchor="center")
    bang.column("XepLoai", width=120, anchor="center")

    thanh_cuon = ttk.Scrollbar(frame_bang, orient="vertical", command=bang.yview)
    bang.configure(yscrollcommand=thanh_cuon.set)
    bang.pack(side="left", fill="both", expand=True)
    thanh_cuon.pack(side="right", fill="y")

    # --- Các hàm logic ---
    def lay_danh_sach():
        for item in bang.get_children():
            bang.delete(item)
        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("SELECT MaSV, MaMon, DiemTX, DiemKT1, DiemKT2, DiemKTHP, DiemTB FROM Diem")
        for dong in cur.fetchall():
            loai = xep_loai(dong[6])
            bang.insert("", "end", values=dong + (loai,))
        conn.close()

    def lam_moi():
        txtMaSV.delete(0, tk.END)
        txtMaMon.delete(0, tk.END)
        txtTX.delete(0, tk.END)
        txtKT1.delete(0, tk.END)
        txtKT2.delete(0, tk.END)
        txtKTHP.delete(0, tk.END)

    def chon_diem(event):
        dong = bang.focus()
        if dong:
            du_lieu = bang.item(dong, "values")
            lam_moi()
            txtMaSV.insert(0, du_lieu[0])
            txtMaMon.insert(0, du_lieu[1])
            txtTX.insert(0, du_lieu[2])
            txtKT1.insert(0, du_lieu[3])
            txtKT2.insert(0, du_lieu[4])
            txtKTHP.insert(0, du_lieu[5])

    bang.bind("<<TreeviewSelect>>", chon_diem)

    def them_diem():
        try:
            ma_sv = txtMaSV.get().strip()
            ma_mon = txtMaMon.get().strip()
            if not ma_sv or not ma_mon:
                messagebox.showwarning("Thông báo", "Hãy nhập mã sinh viên và mã môn!", parent=form)
                return
            tx = float(txtTX.get())
            kt1 = float(txtKT1.get())
            kt2 = float(txtKT2.get())
            kthp = float(txtKTHP.get())

            if any(d < 0 or d > 10 for d in [tx, kt1, kt2, kthp]):
                messagebox.showwarning("Thông báo", "Điểm phải nằm trong khoảng 0 đến 10!", parent=form)
                return

            dtb = tinh_diem_tb(tx, kt1, kt2, kthp)
            conn = ket_noi()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Diem (MaSV, MaMon, DiemTX, DiemKT1, DiemKT2, DiemKTHP, DiemTB)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ma_sv, ma_mon, tx, kt1, kt2, kthp, dtb))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thông báo", f"Thêm điểm thành công!\nĐiểm TB: {dtb}", parent=form)
            lam_moi()
            lay_danh_sach()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ điểm bằng số!", parent=form)
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Điểm môn học này đã tồn tại hoặc mã không hợp lệ!", parent=form)

    def sua_diem():
        try:
            ma_sv = txtMaSV.get().strip()
            ma_mon = txtMaMon.get().strip()
            if not ma_sv or not ma_mon:
                messagebox.showwarning("Thông báo", "Hãy nhập mã sinh viên và mã môn!", parent=form)
                return
            tx = float(txtTX.get())
            kt1 = float(txtKT1.get())
            kt2 = float(txtKT2.get())
            kthp = float(txtKTHP.get())

            if any(d < 0 or d > 10 for d in [tx, kt1, kt2, kthp]):
                messagebox.showwarning("Thông báo", "Điểm phải từ 0 đến 10!", parent=form)
                return

            dtb = tinh_diem_tb(tx, kt1, kt2, kthp)
            conn = ket_noi()
            cur = conn.cursor()
            cur.execute("""
                UPDATE Diem SET DiemTX=?, DiemKT1=?, DiemKT2=?, DiemKTHP=?, DiemTB=?
                WHERE MaSV=? AND MaMon=?
            """, (tx, kt1, kt2, kthp, dtb, ma_sv, ma_mon))
            conn.commit()
            so_dong = cur.rowcount
            conn.close()

            if so_dong == 0:
                messagebox.showwarning("Thông báo", "Không tìm thấy điểm cần sửa!", parent=form)
                return
            messagebox.showinfo("Thông báo", "Cập nhật điểm thành công!", parent=form)
            lam_moi()
            lay_danh_sach()
        except ValueError:
            messagebox.showerror("Lỗi", "Hãy nhập đầy đủ điểm bằng số!", parent=form)

    def xoa_diem():
        ma_sv = txtMaSV.get().strip()
        ma_mon = txtMaMon.get().strip()
        if not ma_sv or not ma_mon:
            messagebox.showwarning("Thông báo", "Hãy chọn điểm cần xóa!", parent=form)
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa điểm này?", parent=form):
            return
        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("DELETE FROM Diem WHERE MaSV=? AND MaMon=?", (ma_sv, ma_mon))
        conn.commit()
        so_dong = cur.rowcount
        conn.close()
        if so_dong == 0:
            messagebox.showwarning("Thông báo", "Không tìm thấy điểm cần xóa!", parent=form)
        else:
            messagebox.showinfo("Thông báo", "Xóa điểm thành công!", parent=form)
            lam_moi()
            lay_danh_sach()

    def tim_diem():
        ma_sv = txtMaSV.get().strip()
        if not ma_sv:
            messagebox.showwarning("Thông báo", "Hãy nhập mã sinh viên cần tìm!", parent=form)
            return
        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("SELECT MaSV, MaMon, DiemTX, DiemKT1, DiemKT2, DiemKTHP, DiemTB FROM Diem WHERE MaSV LIKE ?", ('%' + ma_sv + '%',))
        ket_qua = cur.fetchall()
        conn.close()

        for item in bang.get_children():
            bang.delete(item)
        if len(ket_qua) == 0:
            messagebox.showinfo("Thông báo", "Không tìm thấy điểm của sinh viên!", parent=form)
            return
        for dong in ket_qua:
            loai = xep_loai(dong[6])
            bang.insert("", "end", values=dong + (loai,))

    def xuat_excel():
        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("SELECT MaSV, MaMon, DiemTX, DiemKT1, DiemKT2, DiemKTHP, DiemTB FROM Diem ORDER BY MaSV, MaMon")
        ket_qua = cur.fetchall()
        conn.close()
        if not ket_qua:
            messagebox.showwarning("Thông báo", "Chưa có dữ liệu để xuất Excel!", parent=form)
            return

        duong_dan = filedialog.asksaveasfilename(
            parent=form,
            title="Lưu danh sách điểm",
            defaultextension=".xlsx",
            initialfile="DanhSachDiem.xlsx",
            filetypes=[("Excel", "*.xlsx")],
        )
        if not duong_dan:
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Danh sách điểm"
        ws.append(["Mã sinh viên", "Mã môn", "Điểm TX (10%)", "KT lần 1 (20%)", "KT lần 2 (20%)", "KTHP (50%)", "Điểm TB", "Xếp loại"])

        for dong in ket_qua:
            ma_sv, ma_mon, tx, kt1, kt2, kthp, dtb = dong
            if dtb is None and all(d is not None for d in (tx, kt1, kt2, kthp)):
                dtb = tinh_diem_tb(tx, kt1, kt2, kthp)
            ws.append([ma_sv, ma_mon, tx, kt1, kt2, kthp, dtb, xep_loai(dtb)])

        for o in ws[1]:
            o.font = o.font.copy(bold=True)
        for cot_excel in ws.columns:
            do_rong = max(len(str(o.value or "")) for o in cot_excel)
            ws.column_dimensions[cot_excel[0].column_letter].width = do_rong + 4

        try:
            wb.save(duong_dan)
            messagebox.showinfo("Thành công", f"Xuất Excel thành công!\n{duong_dan}", parent=form)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=form)

    # Đưa các nút lên Hàng 1 & Hàng 2
    tao_nut(hang_nut_1, "✚  Thêm", "#1E8449", them_diem).pack(side="left", padx=5)
    tao_nut(hang_nut_1, "✎  Sửa", "#2E86C1", sua_diem).pack(side="left", padx=5)
    tao_nut(hang_nut_1, "🗑  Xóa", "#CB4335", xoa_diem).pack(side="left", padx=5)
    tao_nut(hang_nut_1, "🔄 Làm mới", "#5D6D7E", lambda: [lam_moi(), lay_danh_sach()]).pack(side="left", padx=5)

    tao_nut(hang_nut_2, "🔍 Tìm kiếm", "#17A2B8", tim_diem).pack(side="left", padx=5)
    tao_nut(hang_nut_2, "📊 Thống kê", "#8E44AD", thong_ke_diem).pack(side="left", padx=5)
    tao_nut(hang_nut_2, "👤 Thống kê SV", "#D35400", thong_ke_sinh_vien).pack(side="left", padx=5)
    tao_nut(hang_nut_2, "📁 Xuất Excel", "#27AE60", xuat_excel).pack(side="left", padx=5)

    lay_danh_sach()
    form.transient()


# =========================================================================
# FORM 2: QUẢN LÝ ĐIỂM DÀNH CHO GIẢNG VIÊN (PHÂN QUYỀN)
# =========================================================================
def mo_form_diem_giang_vien(ma_gv):
    form = tk.Toplevel()
    form.title("QUẢN LÝ ĐIỂM - GIẢNG VIÊN")
    form.geometry("1060x700")
    form.configure(bg="#FFFFFF")
    cau_hinh_style()

    # 1. Khung nhập thông tin
    frame_thong_tin = tk.LabelFrame(
        form,
        text=f" NHẬP ĐIỂM - GIẢNG VIÊN: {ma_gv} ",
        font=("Segoe UI", 11, "bold"),
        bg="#FFFFFF",
        fg="#000000",
        padx=25,
        pady=12,
    )
    frame_thong_tin.pack(fill="x", padx=20, pady=(15, 8))

    frame_thong_tin.columnconfigure(0, weight=0)
    frame_thong_tin.columnconfigure(1, weight=1)
    frame_thong_tin.columnconfigure(2, weight=0)
    frame_thong_tin.columnconfigure(3, weight=1)

    tk.Label(frame_thong_tin, text="Mã sinh viên:", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=0, column=0, padx=(10, 8), pady=6, sticky="e"
    )
    txt_sv = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txt_sv.grid(row=0, column=1, padx=(0, 25), pady=6, sticky="ew")

    tk.Label(frame_thong_tin, text="Mã môn học:", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=0, column=2, padx=(10, 8), pady=6, sticky="e"
    )
    txt_mon = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txt_mon.grid(row=0, column=3, padx=(0, 10), pady=6, sticky="ew")

    tk.Label(frame_thong_tin, text="Điểm TX (10%):", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=1, column=0, padx=(10, 8), pady=6, sticky="e"
    )
    txt_tx = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txt_tx.grid(row=1, column=1, padx=(0, 25), pady=6, sticky="ew")

    tk.Label(frame_thong_tin, text="Kiểm tra lần 1 (20%):", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=1, column=2, padx=(10, 8), pady=6, sticky="e"
    )
    txt_kt1 = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txt_kt1.grid(row=1, column=3, padx=(0, 10), pady=6, sticky="ew")

    tk.Label(frame_thong_tin, text="Kiểm tra lần 2 (20%):", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=2, column=0, padx=(10, 8), pady=6, sticky="e"
    )
    txt_kt2 = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txt_kt2.grid(row=2, column=1, padx=(0, 25), pady=6, sticky="ew")

    tk.Label(frame_thong_tin, text="Kết thúc HP (50%):", font=("Segoe UI", 10), bg="#FFFFFF").grid(
        row=2, column=2, padx=(10, 8), pady=6, sticky="e"
    )
    txt_kthp = tk.Entry(frame_thong_tin, font=("Segoe UI", 10), relief="solid", bd=1)
    txt_kthp.grid(row=2, column=3, padx=(0, 10), pady=6, sticky="ew")

    # 2. Khung nút chức năng
    frame_nut = tk.Frame(form, bg="#FFFFFF")
    frame_nut.pack(pady=8)

    # 3. Khung bảng danh sách
    frame_bang = tk.LabelFrame(
        form,
        text=" DANH SÁCH ĐIỂM THEO PHÂN CÔNG GIẢNG DẠY ",
        font=("Segoe UI", 11, "bold"),
        bg="#FFFFFF",
        fg="#000000",
        padx=10,
        pady=10,
    )
    frame_bang.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    cot = ("MaSV", "MaMon", "DiemTX", "DiemKT1", "DiemKT2", "DiemKTHP", "DiemTB", "XepLoai")
    bang_gv = ttk.Treeview(frame_bang, columns=cot, show="headings")

    ten_cot = ["Mã SV", "Mã môn", "Điểm TX", "KT lần 1", "KT lần 2", "KTHP", "Điểm TB", "Xếp loại"]
    for i, ten in enumerate(ten_cot):
        bang_gv.heading(cot[i], text=ten)
        bang_gv.column(cot[i], width=110, anchor="center")
    bang_gv.column("XepLoai", width=120, anchor="center")

    thanh_cuon = ttk.Scrollbar(frame_bang, orient="vertical", command=bang_gv.yview)
    bang_gv.configure(yscrollcommand=thanh_cuon.set)
    bang_gv.pack(side="left", fill="both", expand=True)
    thanh_cuon.pack(side="right", fill="y")

    # --- Logic xử lý ---
    def kiem_tra_phan_cong(ma_sv, ma_mon):
        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM SinhVien sv
            INNER JOIN PhanCong pc ON sv.MaLop = pc.MaLop
            WHERE sv.MaSV = ? AND pc.MaMon = ? AND pc.MaGV = ?
        """, (ma_sv, ma_mon, ma_gv))
        ket_qua = cur.fetchone()[0]
        conn.close()
        return ket_qua > 0

    def lay_danh_sach_gv(tu_khoa=""):
        for item in bang_gv.get_children():
            bang_gv.delete(item)
        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT d.MaSV, d.MaMon, d.DiemTX, d.DiemKT1, d.DiemKT2, d.DiemKTHP, d.DiemTB
            FROM Diem d
            INNER JOIN SinhVien sv ON d.MaSV = sv.MaSV
            INNER JOIN PhanCong pc ON sv.MaLop = pc.MaLop AND d.MaMon = pc.MaMon
            WHERE pc.MaGV = ? AND (d.MaSV LIKE ? OR d.MaMon LIKE ?)
            ORDER BY d.MaSV, d.MaMon
        """, (ma_gv, "%" + tu_khoa + "%", "%" + tu_khoa + "%"))
        danh_sach = cur.fetchall()
        conn.close()

        for dong in danh_sach:
            dtb = dong[6]
            if dtb is None and all(d is not None for d in dong[2:6]):
                dtb = tinh_diem_tb(*dong[2:6])
            bang_gv.insert("", "end", values=(
                dong[0], dong[1], dong[2], dong[3], dong[4], dong[5],
                f"{dtb:.2f}" if dtb is not None else "Chưa có",
                xep_loai(dtb)
            ))

    def lam_moi_gv():
        for o in (txt_sv, txt_mon, txt_tx, txt_kt1, txt_kt2, txt_kthp):
            o.delete(0, tk.END)
        lay_danh_sach_gv()

    def chon_diem_gv(event):
        dong = bang_gv.focus()
        if dong:
            du_lieu = bang_gv.item(dong, "values")
            for o in (txt_sv, txt_mon, txt_tx, txt_kt1, txt_kt2, txt_kthp):
                o.delete(0, tk.END)
            txt_sv.insert(0, du_lieu[0])
            txt_mon.insert(0, du_lieu[1])
            for o, val in zip([txt_tx, txt_kt1, txt_kt2, txt_kthp], du_lieu[2:6]):
                if val != "None":
                    o.insert(0, val)

    bang_gv.bind("<<TreeviewSelect>>", chon_diem_gv)

    def lay_thong_tin_diem():
        ma_sv = txt_sv.get().strip()
        ma_mon = txt_mon.get().strip()
        if not ma_sv or not ma_mon:
            messagebox.showwarning("Thông báo", "Hãy nhập mã sinh viên và mã môn!", parent=form)
            return None
        if not kiem_tra_phan_cong(ma_sv, ma_mon):
            messagebox.showerror("Không có quyền", "Bạn không được phân công lớp hoặc môn này!", parent=form)
            return None
        try:
            tx = float(txt_tx.get())
            kt1 = float(txt_kt1.get())
            kt2 = float(txt_kt2.get())
            kthp = float(txt_kthp.get())
            if any(d < 0 or d > 10 for d in [tx, kt1, kt2, kthp]):
                messagebox.showwarning("Thông báo", "Điểm phải từ 0 đến 10!", parent=form)
                return None
            return ma_sv, ma_mon, tx, kt1, kt2, kthp, tinh_diem_tb(tx, kt1, kt2, kthp)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ điểm bằng số!", parent=form)
            return None

    def them_diem_gv():
        dl = lay_thong_tin_diem()
        if dl is None:
            return
        try:
            conn = ket_noi()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Diem (MaSV, MaMon, DiemTX, DiemKT1, DiemKT2, DiemKTHP, DiemTB)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, dl)
            conn.commit()
            conn.close()
            messagebox.showinfo("Thông báo", "Thêm điểm thành công!", parent=form)
            lam_moi_gv()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Điểm môn này đã tồn tại!", parent=form)

    def sua_diem_gv():
        dl = lay_thong_tin_diem()
        if dl is None:
            return
        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Diem SET DiemTX=?, DiemKT1=?, DiemKT2=?, DiemKTHP=?, DiemTB=?
            WHERE MaSV=? AND MaMon=?
        """, (dl[2], dl[3], dl[4], dl[5], dl[6], dl[0], dl[1]))
        so_dong = cur.rowcount
        conn.commit()
        conn.close()
        if so_dong > 0:
            messagebox.showinfo("Thông báo", "Cập nhật thành công!", parent=form)
            lam_moi_gv()
        else:
            messagebox.showwarning("Thông báo", "Không tìm thấy điểm!", parent=form)

    def xoa_diem_gv():
        ma_sv = txt_sv.get().strip()
        ma_mon = txt_mon.get().strip()
        if not ma_sv or not ma_mon:
            messagebox.showwarning("Thông báo", "Hãy chọn điểm cần xóa!", parent=form)
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa điểm này?", parent=form):
            return
        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("DELETE FROM Diem WHERE MaSV=? AND MaMon=?", (ma_sv, ma_mon))
        so_dong = cur.rowcount
        conn.commit()
        conn.close()
        if so_dong > 0:
            messagebox.showinfo("Thông báo", "Xóa thành công!", parent=form)
            lam_moi_gv()
        else:
            messagebox.showwarning("Thông báo", "Không tìm thấy điểm!", parent=form)

    def tim_diem_gv():
        tu_khoa = txt_sv.get().strip() or txt_mon.get().strip()
        if not tu_khoa:
            messagebox.showwarning("Thông báo", "Hãy nhập mã SV hoặc mã môn cần tìm!", parent=form)
            return
        lay_danh_sach_gv(tu_khoa)

    def xuat_excel_gv():
        conn = ket_noi()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT d.MaSV, d.MaMon, d.DiemTX, d.DiemKT1, d.DiemKT2, d.DiemKTHP, d.DiemTB
            FROM Diem d
            INNER JOIN SinhVien sv ON d.MaSV = sv.MaSV
            INNER JOIN PhanCong pc ON sv.MaLop = pc.MaLop AND d.MaMon = pc.MaMon
            WHERE pc.MaGV = ? ORDER BY d.MaSV, d.MaMon
        """, (ma_gv,))
        danh_sach = cur.fetchall()
        conn.close()
        if not danh_sach:
            messagebox.showinfo("Thông báo", "Chưa có dữ liệu điểm để xuất!", parent=form)
            return
        duong_dan = filedialog.asksaveasfilename(
            parent=form,
            title="Lưu danh sách điểm",
            defaultextension=".xlsx",
            initialfile="Diem_GiangVien.xlsx",
            filetypes=[("Excel", "*.xlsx")],
        )
        if not duong_dan:
            return
        wb = Workbook()
        ws = wb.active
        ws.title = "Danh sách điểm"
        ws.append(["Mã sinh viên", "Mã môn", "Điểm TX", "Kiểm tra 1", "Kiểm tra 2", "Kết thúc HP", "Điểm trung bình", "Xếp loại"])
        for dong in danh_sach:
            dtb = dong[6]
            if dtb is None and all(d is not None for d in dong[2:6]):
                dtb = tinh_diem_tb(*dong[2:6])
            ws.append(list(dong[:6]) + [dtb, xep_loai(dtb)])
        try:
            wb.save(duong_dan)
            messagebox.showinfo("Thành công", "Xuất Excel thành công!", parent=form)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=form)

    # Đưa các nút bấm vào khung chức năng
    tao_nut(frame_nut, "✚  Thêm", "#1E8449", them_diem_gv).pack(side="left", padx=5)
    tao_nut(frame_nut, "✎  Sửa", "#2E86C1", sua_diem_gv).pack(side="left", padx=5)
    tao_nut(frame_nut, "🗑  Xóa", "#CB4335", xoa_diem_gv).pack(side="left", padx=5)
    tao_nut(frame_nut, "🔍 Tìm kiếm", "#17A2B8", tim_diem_gv).pack(side="left", padx=5)
    tao_nut(frame_nut, "🔄 Làm mới", "#5D6D7E", lam_moi_gv).pack(side="left", padx=5)
    tao_nut(frame_nut, "📁 Xuất Excel", "#27AE60", xuat_excel_gv).pack(side="left", padx=5)

    # Kiểm tra quyền phân công
    conn = ket_noi()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM PhanCong WHERE MaGV = ?", (ma_gv,))
    so_phan_cong = cur.fetchone()[0]
    conn.close()
    if so_phan_cong == 0:
        messagebox.showwarning("Thông báo", "Giảng viên chưa được phân công lớp và môn học nào!", parent=form)
        return

    lay_danh_sach_gv()
    form.transient()


# =========================================================================
# CỬA SỔ PHỤ: THỐNG KÊ
# =========================================================================
def thong_ke_diem():
    cua_so = tk.Toplevel()
    cua_so.title("THỐNG KÊ ĐIỂM")
    cua_so.geometry("1060x520")
    cua_so.configure(bg="#FFFFFF")
    cau_hinh_style()

    conn = ket_noi()
    cur = conn.cursor()
    cur.execute("SELECT MaSV, MaMon, DiemTX, DiemKT1, DiemKT2, DiemKTHP, DiemTB FROM Diem ORDER BY MaSV, MaMon")
    danh_sach = cur.fetchall()
    conn.close()

    if not danh_sach:
        tk.Label(cua_so, text="Chưa có dữ liệu điểm!", font=("Segoe UI", 12), bg="#FFFFFF").pack(pady=20)
        return

    ds_diem = []
    for dong in danh_sach:
        dtb = dong[6]
        if dtb is None and all(d is not None for d in dong[2:6]):
            dtb = tinh_diem_tb(*dong[2:6])
        if dtb is not None:
            ds_diem.append(dtb)

    if ds_diem:
        tk.Label(
            cua_so,
            text=f"Số lượt điểm: {len(ds_diem)}  |  Điểm TB chung: {sum(ds_diem)/len(ds_diem):.2f}  |  Cao nhất: {max(ds_diem):.2f}  |  Thấp nhất: {min(ds_diem):.2f}",
            font=("Segoe UI", 11, "bold"),
            bg="#EAF2F8",
            fg="#1A5276",
            pady=8,
        ).pack(fill="x", padx=15, pady=10)

    khung = tk.Frame(cua_so, bg="#FFFFFF")
    khung.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    cot = ("MaSV", "MaMon", "DiemTX", "DiemKT1", "DiemKT2", "DiemKTHP", "DiemTB", "XepLoai")
    bang_diem = ttk.Treeview(khung, columns=cot, show="headings")
    ten_cot = ["Mã SV", "Mã môn", "Điểm TX", "KT lần 1", "KT lần 2", "KTHP", "Điểm TB", "Xếp loại"]
    for i, ten in enumerate(ten_cot):
        bang_diem.heading(cot[i], text=ten)
        bang_diem.column(cot[i], width=110, anchor="center")

    thanh_cuon = ttk.Scrollbar(khung, orient="vertical", command=bang_diem.yview)
    bang_diem.configure(yscrollcommand=thanh_cuon.set)
    bang_diem.pack(side="left", fill="both", expand=True)
    thanh_cuon.pack(side="right", fill="y")

    for dong in danh_sach:
        ma_sv, ma_mon, tx, kt1, kt2, kthp, dtb = dong
        if dtb is None and all(d is not None for d in (tx, kt1, kt2, kthp)):
            dtb = tinh_diem_tb(tx, kt1, kt2, kthp)
        bang_diem.insert("", "end", values=(
            ma_sv, ma_mon, tx, kt1, kt2, kthp,
            f"{dtb:.2f}" if dtb is not None else "Chưa có",
            xep_loai(dtb)
        ))


def thong_ke_sinh_vien():
    ma_sv = txtMaSV.get().strip()
    if not ma_sv:
        messagebox.showwarning("Thông báo", "Hãy nhập mã sinh viên cần thống kê!", parent=txtMaSV.winfo_toplevel())
        return

    conn = ket_noi()
    cur = conn.cursor()
    cur.execute("SELECT MaMon, DiemTX, DiemKT1, DiemKT2, DiemKTHP, DiemTB FROM Diem WHERE MaSV = ?", (ma_sv,))
    ket_qua = cur.fetchall()
    conn.close()

    if not ket_qua:
        messagebox.showinfo("Thông báo", "Sinh viên chưa có điểm môn học nào!", parent=txtMaSV.winfo_toplevel())
        return

    tong_diem = 0
    dem = 0
    noi_dung = f"Mã sinh viên: {ma_sv}\nSố môn học: {len(ket_qua)}\n" + "-" * 40 + "\n"
    for dong in ket_qua:
        ma_mon = dong[0]
        dtb = dong[5]
        if dtb is None and all(d is not None for d in dong[1:5]):
            dtb = tinh_diem_tb(*dong[1:5])
        if dtb is not None:
            tong_diem += dtb
            dem += 1
            noi_dung += f"Môn: {ma_mon} | TB: {dtb:.2f} | Xếp loại: {xep_loai(dtb)}\n"

    if dem > 0:
        noi_dung += "-" * 40 + f"\nĐiểm trung bình tích lũy: {tong_diem / dem:.2f}"
    messagebox.showinfo("THỐNG KÊ SINH VIÊN", noi_dung)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mo_form_diem()
    root.mainloop()