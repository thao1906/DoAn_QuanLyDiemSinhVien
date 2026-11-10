import tkinter as tk
import frm_SinhVien
import frm_Lop
import frm_Diem
import frm_MonHoc
import frm_GiangVien
import frm_TaiKhoan
import frm_PhanCong
import frm_DoiMatKhau
import sys
import sqlite3
from tkinter import ttk

from tkinter import messagebox

# Tao cua so chinh
root = tk.Tk()
root.title("QUẢN LÝ ĐIỂM SINH VIÊN")
root.geometry("900x600")
root.configure(bg="#EAF2F8")

# Nhận thông tin tài khoản đăng nhập
ten_dang_nhap = sys.argv[1] if len(sys.argv) > 1 else ""
vai_tro = sys.argv[2] if len(sys.argv) > 2 else "Admin"
ma_gv = sys.argv[3] if len(sys.argv) > 3 else ""
ma_sv = sys.argv[4] if len(sys.argv) > 4 else ""

def xem_diem_ca_nhan(ma_sv):
    if not ma_sv:
        messagebox.showerror(
            "Lỗi",
            "Tài khoản chưa được liên kết với mã sinh viên!"
        )
        return

    form = tk.Toplevel()
    form.title("KẾT QUẢ HỌC TẬP CÁ NHÂN")
    form.geometry("1150x650")

    tk.Label(
        form,
        text="BẢNG ĐIỂM CÁ NHÂN",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(
        form,
        text="Mã sinh viên: " + ma_sv,
        font=("Arial", 12)
    ).pack(pady=5)

    # Ham xep loai
    def xep_loai(diem):
        if diem >= 9:
            return "Xuất sắc"
        elif diem >= 8:
            return "Giỏi"
        elif diem >= 7:
            return "Khá"
        elif diem >= 5:
            return "Trung bình"
        else:
            return "Yếu"

    khung = tk.Frame(form)
    khung.pack(fill="both", expand=True, padx=15, pady=15)

    cot = (
        "MaMon", "TenMon", "DiemTX",
        "DiemKT1", "DiemKT2", "DiemKTHP",
        "DiemTB", "XepLoai"
    )

    bang = ttk.Treeview(
        khung,
        columns=cot,
        show="headings"
    )

    ten_cot = {
        "MaMon": "Mã môn",
        "TenMon": "Tên môn",
        "DiemTX": "Điểm TX",
        "DiemKT1": "Điểm KT1",
        "DiemKT2": "Điểm KT2",
        "DiemKTHP": "Điểm KTHP",
        "DiemTB": "Điểm TB",
        "XepLoai": "Xếp loại"
    }

    for c in cot:
        bang.heading(c, text=ten_cot[c])
        bang.column(c, width=130, anchor="center")

    thanh_cuon = ttk.Scrollbar(
        khung,
        orient="vertical",
        command=bang.yview
    )

    bang.configure(yscrollcommand=thanh_cuon.set)

    bang.pack(side="left", fill="both", expand=True)
    thanh_cuon.pack(side="right", fill="y")

    try:
        conn = sqlite3.connect("QLD.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT d.MaMon, m.TenMon,
                   d.DiemTX, d.DiemKT1,
                   d.DiemKT2, d.DiemKTHP,
                   d.DiemTB
            FROM Diem d
            JOIN MonHoc m ON d.MaMon = m.MaMon
            WHERE d.MaSV = ?
        """, (ma_sv,))

        ds = cur.fetchall()
        conn.close()

        danh_sach_diem = []

        for dong in ds:
            diem_tb = dong[6]

            if diem_tb is not None:
                diem_tb = float(diem_tb)
                loai = xep_loai(diem_tb)
                danh_sach_diem.append(diem_tb)
            else:
                loai = "Chưa có"

            bang.insert(
                "",
                "end",
                values=dong + (loai,)
            )

        if danh_sach_diem:
            diem_tb_chung = sum(danh_sach_diem) / len(danh_sach_diem)

            tk.Label(
                form,
                text="Điểm trung bình chung: {:.2f}".format(
                    diem_tb_chung
                ),
                font=("Arial", 13, "bold"),
                fg="blue"
            ).pack(pady=5)

            tk.Label(
                form,
                text="Xếp loại học lực: " + xep_loai(diem_tb_chung),
                font=("Arial", 13, "bold"),
                fg="green"
            ).pack(pady=5)

        else:
            tk.Label(
                form,
                text="Sinh viên chưa có điểm!",
                font=("Arial", 12),
                fg="red"
            ).pack(pady=10)

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
menubar = tk.Menu(root)

# Menu hệ thống
menu_he_thong = tk.Menu(menubar, tearoff=0)

menu_he_thong.add_command(
    label="Trang chủ",
    command=lambda: messagebox.showinfo(
        "Thông báo", "Đây là trang chủ"
    )
)

menu_he_thong.add_separator()
menu_he_thong.add_command(
    label="Thoát",
    command=root.destroy
)

menubar.add_cascade(
    label="Hệ thống",
    menu=menu_he_thong
)

# Menu quản lý
menu_quan_ly = tk.Menu(menubar, tearoff=0)

if vai_tro == "Admin":

    menu_quan_ly.add_command(
        label="Quản lý lớp",
        command=frm_Lop.mo_form_lop
    )

    menu_quan_ly.add_command(
        label="Quản lý sinh viên",
        command=frm_SinhVien.mo_form_sinh_vien
    )

    menu_quan_ly.add_command(
        label="Quản lý giảng viên",
        command=frm_GiangVien.mo_form_giang_vien
    )

    menu_quan_ly.add_command(
        label="Phân công giảng dạy",
        command=frm_PhanCong.mo_form_phan_cong
    )

    menu_quan_ly.add_command(
        label="Quản lý môn học",
        command=frm_MonHoc.mo_form_mon_hoc
    )

    menu_quan_ly.add_command(
        label="Quản lý điểm",
        command=frm_Diem.mo_form_diem
    )

    menu_quan_ly.add_command(
        label="Quản lý tài khoản",
        command=frm_TaiKhoan.mo_form_tai_khoan
    )

elif vai_tro == "GiangVien":

    # Tạm thời chỉ mở chức năng xem điểm
    menu_quan_ly.add_command(
        label="Xem danh sách điểm",
        command=frm_Diem.mo_form_diem_giang_vien(ma_gv)
    )

    menu_quan_ly.add_command(
    label="Đổi mật khẩu",
    command=lambda: frm_DoiMatKhau.mo_form_doi_mat_khau(ten_dang_nhap)
)

elif vai_tro == "SinhVien":

    # Sinh viên chỉ xem điểm của mình
    menu_quan_ly.add_command(
        label="Xem điểm cá nhân",
        command=lambda: xem_diem_ca_nhan(ma_sv)
    )
    menu_quan_ly.add_command(
    label="Đổi mật khẩu",
    command=lambda: frm_DoiMatKhau.mo_form_doi_mat_khau(ten_dang_nhap)
)

menubar.add_cascade(
    label="Quản lý",
    menu=menu_quan_ly
)

# Menu thống kê: chỉ Admin
if vai_tro == "Admin":

    menu_thong_ke = tk.Menu(menubar, tearoff=0)

    menu_thong_ke.add_command(
        label="Thống kê điểm",
        command=frm_Diem.thong_ke_diem
    )

    menu_thong_ke.add_command(
        label="Thống kê điểm trung bình",
        command=frm_Diem.tinh_diem_tb
    )

    menubar.add_cascade(
        label="Thống kê",
        menu=menu_thong_ke
    )

root.config(menu=menubar)
# Tieu de

import tkinter as tk

# Phần trang chủ
trang_chu = tk.Frame(root, bg="#F2F2F2")
trang_chu.pack(fill="both", expand=True)

# Tiêu đề báo cáo
tk.Label(
    trang_chu,
    text="BÁO CÁO ĐỒ ÁN\nChuyên đề Python",
    font=("Arial", 25, "bold"),
    bg="#F2F2F2",
    fg="black",
    justify="center"
).pack(pady=(40, 20))

# Tên đề tài
tk.Label(
    trang_chu,
    text="Đề tài: XÂY DỰNG ỨNG DỤNG\nQUẢN LÝ ĐIỂM SINH VIÊN\nVỚI PYTHON, TKINTER VÀ SQLITE3",
    font=("Arial", 21, "bold"),
    bg="#F2F2F2",
    fg="black",
    justify="center"
).pack(pady=10)

# Giảng viên hướng dẫn
tk.Label(
    trang_chu,
    text="Giảng viên hướng dẫn\nThS. Nguyễn Ngọc Minh",
    font=("Arial", 13),
    bg="#F2F2F2",
    justify="center"
).pack(pady=(15, 10))

# Thông tin sinh viên
tk.Label(
    trang_chu,
    text="Sinh viên thực hiện: Nguyễn Thị Ái Tiền - DTH245910\n"
         "Sinh viên thực hiện: Lâm Kim Thảo - DTH245888\n",
    font=("Arial", 13),
    bg="#F2F2F2",
    justify="center"
).pack(pady=5)

# Tên cơ sở dữ liệu
tk.Label(
    trang_chu,
    text="Cơ sở dữ liệu: QLD.db (SQLite3)",
    font=("Arial", 11, "italic"),
    bg="#F2F2F2"
).pack(pady=20)


# Chay chuong trinh
root.mainloop()