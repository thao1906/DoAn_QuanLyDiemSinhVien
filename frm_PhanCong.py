
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

DUONG_DAN_DB = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "QLD.db"
)


def ket_noi():
    return sqlite3.connect(DUONG_DAN_DB)


def tao_bang_phan_cong():
    conn = ket_noi()
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhanCong (
            MaGV TEXT NOT NULL,
            MaLop TEXT NOT NULL,
            MaMon TEXT NOT NULL,

            PRIMARY KEY (MaGV, MaLop, MaMon),

            FOREIGN KEY (MaGV)
                REFERENCES GiangVien(MaGV),

            FOREIGN KEY (MaLop)
                REFERENCES Lop(MaLop),

            FOREIGN KEY (MaMon)
                REFERENCES MonHoc(MaMon)
        )
    """)

    conn.commit()
    conn.close()


def mo_form_phan_cong():
    tao_bang_phan_cong()

    form = tk.Toplevel()
    form.title("PHÂN CÔNG GIẢNG DẠY")
    form.geometry("950x600")
    form.configure(bg="#EAF2F8")

    tk.Label(
        form,
        text="PHÂN CÔNG GIẢNG DẠY",
        font=("Arial", 18, "bold"),
        bg="#EAF2F8",
        fg="#1A5276"
    ).pack(pady=15)

    khung = tk.Frame(form, bg="#EAF2F8")
    khung.pack(pady=10)

    # Mã giảng viên
    tk.Label(
        khung,
        text="Giảng viên:",
        bg="#EAF2F8",
        width=15,
        anchor="w"
    ).grid(row=0, column=0, padx=5, pady=8)

    cbo_gv = ttk.Combobox(
        khung,
        width=35,
        state="readonly"
    )
    cbo_gv.grid(row=0, column=1, padx=5, pady=8)

    # Mã lớp
    tk.Label(
        khung,
        text="Lớp:",
        bg="#EAF2F8",
        width=15,
        anchor="w"
    ).grid(row=1, column=0, padx=5, pady=8)

    cbo_lop = ttk.Combobox(
        khung,
        width=35,
        state="readonly"
    )
    cbo_lop.grid(row=1, column=1, padx=5, pady=8)

    # Mã môn
    tk.Label(
        khung,
        text="Môn học:",
        bg="#EAF2F8",
        width=15,
        anchor="w"
    ).grid(row=2, column=0, padx=5, pady=8)

    cbo_mon = ttk.Combobox(
        khung,
        width=35,
        state="readonly"
    )
    cbo_mon.grid(row=2, column=1, padx=5, pady=8)

    # Bảng phân công
    khung_bang = tk.Frame(form)
    khung_bang.pack(fill="both", expand=True, padx=15, pady=10)

    cot = ("MaGV", "HoTen", "MaLop", "TenLop", "MaMon", "TenMon")

    bang = ttk.Treeview(
        khung_bang,
        columns=cot,
        show="headings"
    )

    ten_cot = [
        "Mã GV",
        "Tên giảng viên",
        "Mã lớp",
        "Tên lớp",
        "Mã môn",
        "Tên môn"
    ]

    for i, ten in enumerate(ten_cot):
        bang.heading(cot[i], text=ten)
        bang.column(cot[i], width=140, anchor="center")

    thanh_cuon = ttk.Scrollbar(
        khung_bang,
        orient="vertical",
        command=bang.yview
    )

    bang.configure(yscrollcommand=thanh_cuon.set)

    bang.pack(side="left", fill="both", expand=True)
    thanh_cuon.pack(side="right", fill="y")

    def tai_du_lieu_combobox():
        conn = ket_noi()
        cur = conn.cursor()

        cur.execute("""
            SELECT MaGV, HoTen
            FROM GiangVien
            ORDER BY MaGV
        """)
        ds_gv = cur.fetchall()

        cur.execute("""
            SELECT MaLop, TenLop
            FROM Lop
            ORDER BY MaLop
        """)
        ds_lop = cur.fetchall()

        cur.execute("""
            SELECT MaMon, TenMon
            FROM MonHoc
            ORDER BY MaMon
        """)
        ds_mon = cur.fetchall()

        conn.close()

        cbo_gv["values"] = [
            ma + " - " + ten for ma, ten in ds_gv
        ]

        cbo_lop["values"] = [
            ma + " - " + ten for ma, ten in ds_lop
        ]

        cbo_mon["values"] = [
            ma + " - " + ten for ma, ten in ds_mon
        ]

    def lay_danh_sach():
        for item in bang.get_children():
            bang.delete(item)

        conn = ket_noi()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                pc.MaGV, gv.HoTen,
                pc.MaLop, l.TenLop,
                pc.MaMon, mh.TenMon
            FROM PhanCong pc
            JOIN GiangVien gv ON pc.MaGV = gv.MaGV
            JOIN Lop l ON pc.MaLop = l.MaLop
            JOIN MonHoc mh ON pc.MaMon = mh.MaMon
            ORDER BY pc.MaGV, pc.MaLop, pc.MaMon
        """)

        danh_sach = cur.fetchall()
        conn.close()

        for dong in danh_sach:
            bang.insert("", "end", values=dong)

    def lam_moi():
        cbo_gv.set("")
        cbo_lop.set("")
        cbo_mon.set("")

    def them_phan_cong():
        gv = cbo_gv.get()
        lop = cbo_lop.get()
        mon = cbo_mon.get()

        if gv == "" or lop == "" or mon == "":
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn đầy đủ giảng viên, lớp và môn học!",
                parent=form
            )
            return

        ma_gv = gv.split(" - ")[0]
        ma_lop = lop.split(" - ")[0]
        ma_mon = mon.split(" - ")[0]

        try:
            conn = ket_noi()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO PhanCong (MaGV, MaLop, MaMon)
                VALUES (?, ?, ?)
            """, (ma_gv, ma_lop, ma_mon))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Thông báo",
                "Phân công giảng dạy thành công!",
                parent=form
            )

            lam_moi()
            lay_danh_sach()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Lỗi",
                "Phân công này đã tồn tại hoặc mã liên kết không hợp lệ!",
                parent=form
            )

        except sqlite3.Error as e:
            messagebox.showerror(
                "Lỗi cơ sở dữ liệu",
                str(e),
                parent=form
            )

    def xoa_phan_cong():
        dong = bang.focus()

        if not dong:
            messagebox.showwarning(
                "Thông báo",
                "Hãy chọn phân công cần xóa!",
                parent=form
            )
            return

        du_lieu = bang.item(dong, "values")

        if not messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn xóa phân công này không?",
            parent=form
        ):
            return

        conn = ket_noi()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM PhanCong
            WHERE MaGV = ? AND MaLop = ? AND MaMon = ?
        """, (du_lieu[0], du_lieu[2], du_lieu[4]))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Thông báo",
            "Xóa phân công thành công!",
            parent=form
        )

        lay_danh_sach()
        lam_moi()

    def chon_phan_cong(event):
        dong = bang.focus()

        if dong:
            du_lieu = bang.item(dong, "values")

            cbo_gv.set(du_lieu[0] + " - " + du_lieu[1])
            cbo_lop.set(du_lieu[2] + " - " + du_lieu[3])
            cbo_mon.set(du_lieu[4] + " - " + du_lieu[5])

    bang.bind("<<TreeviewSelect>>", chon_phan_cong)

    # ==========================
    # NÚT CHỨC NĂNG
    # ==========================

    khung_nut = tk.Frame(
        form,
        bg="#EAF2F8"
    )

    khung_nut.pack(
        pady=12
    )

    btn_container = tk.Frame(
        khung_nut,
        bg="#EAF2F8"
    )

    btn_container.pack()


    def tao_nut(text, command, color, width=18):

        return tk.Button(
            btn_container,
            text=text,
            command=command,
            width=width,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            height=2
        )


    tao_nut(
        "➕ Thêm phân công",
        them_phan_cong,
        "#16A34A"
    ).pack(
        side="left",
        padx=8
    )

    tao_nut(
        "🗑 Xóa phân công",
        xoa_phan_cong,
        "#DC2626"
    ).pack(
        side="left",
        padx=8
    )

    tao_nut(
        "🔄 Làm mới",
        lam_moi,
        "#64748B",
        width=15
    ).pack(
        side="left",
        padx=8
    )

    tai_du_lieu_combobox()
    lay_danh_sach()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mo_form_phan_cong()
    root.mainloop()