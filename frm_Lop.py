import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def ket_noi():
    return sqlite3.connect("QLD.db")


def mo_form_lop():

    form = tk.Toplevel()
    form.title("QUẢN LÝ LỚP")
    form.geometry("950x650")
    form.configure(bg="#F8FAFC")

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except:
        pass

    style.configure(
        "Treeview",
        rowheight=30,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold")
    )

    frame_input = tk.LabelFrame(
        form,
        text=" THÔNG TIN LỚP ",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        padx=15,
        pady=15
    )

    frame_input.pack(
        fill="x",
        padx=15,
        pady=(20,10)
    )

    khung_nhap = tk.Frame(
        frame_input,
        bg="white"
    )

    khung_nhap.pack()

    tk.Label(
        khung_nhap,
        text="Mã lớp",
        bg="white",
        font=("Segoe UI", 10)
    ).grid(
        row=0,
        column=0,
        padx=(20, 10),
        pady=10
    )

    txt_ma = ttk.Entry(
        khung_nhap,
        width=25
    )

    txt_ma.grid(
        row=0,
        column=1,
        padx=(0, 30)
    )

    tk.Label(
        khung_nhap,
        text="Tên lớp",
        bg="white",
        font=("Segoe UI", 10)
    ).grid(
        row=0,
        column=2,
        padx=(0, 10),
        pady=10
    )

    txt_ten = ttk.Entry(
        khung_nhap,
        width=40
    )

    txt_ten.grid(
        row=0,
        column=3,
        padx=(0, 20)
    )

    def xoa_trang():
        txt_ma.delete(0, tk.END)
        txt_ten.delete(0, tk.END)

    def tai_danh_sach():

        for item in bang.get_children():
            bang.delete(item)

        conn = ket_noi()
        cur = conn.cursor()

        cur.execute("""
            SELECT MaLop, TenLop
            FROM Lop
            ORDER BY MaLop
        """)

        for dong in cur.fetchall():
            bang.insert(
                "",
                "end",
                values=dong
            )

        conn.close()

    def them():

        ma = txt_ma.get().strip()
        ten = txt_ten.get().strip()

        if not ma or not ten:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng nhập đầy đủ thông tin!"
            )
            return

        try:
            conn = ket_noi()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO Lop(MaLop, TenLop)
                VALUES (?, ?)
                """,
                (ma, ten)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Thông báo",
                "Thêm lớp thành công!"
            )

            xoa_trang()
            tai_danh_sach()

        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                str(e)
            )

    def sua():

        ma = txt_ma.get().strip()
        ten = txt_ten.get().strip()

        if not ma or not ten:
            messagebox.showwarning(
                "Thông báo",
                "Hãy chọn lớp cần sửa!"
            )
            return

        conn = ket_noi()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE Lop
            SET TenLop=?
            WHERE MaLop=?
            """,
            (ten, ma)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Thông báo",
            "Cập nhật thành công!"
        )

        tai_danh_sach()

    def xoa():

        ma = txt_ma.get().strip()

        if not ma:
            messagebox.showwarning(
                "Thông báo",
                "Hãy chọn lớp cần xóa!"
            )
            return

        if not messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn xóa lớp này không?"
        ):
            return

        conn = ket_noi()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM Lop WHERE MaLop=?",
            (ma,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Thông báo",
            "Xóa lớp thành công!"
        )

        xoa_trang()
        tai_danh_sach()

    def chon_dong(event):

        dong = bang.focus()

        if dong:

            du_lieu = bang.item(
                dong,
                "values"
            )

            xoa_trang()

            txt_ma.insert(
                0,
                du_lieu[0]
            )

            txt_ten.insert(
                0,
                du_lieu[1]
            )

    # ==========================
    # NÚT CHỨC NĂNG
    # ==========================

    frame_btn = tk.Frame(
        form,
        bg="#F8FAFC"
    )

    frame_btn.pack(
        fill="x",
        pady=10
    )

    btn_container = tk.Frame(
        frame_btn,
        bg="#F8FAFC"
    )

    btn_container.pack()

    def tao_nut(text, command, color):

        return tk.Button(
            btn_container,
            text=text,
            command=command,
            bg=color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=15,
            height=2,
            relief="flat",
            cursor="hand2"
        )

    tao_nut("➕ Thêm",them,"#16A34A").pack(side="left", padx=8)

    tao_nut("✏️ Sửa",sua,"#2563EB").pack(side="left", padx=8)

    tao_nut("🗑 Xóa",xoa,"#DC2626").pack(side="left", padx=8)

    tao_nut("🔄 Làm mới",lambda: [xoa_trang(), tai_danh_sach()],"#64748B"
            ).pack(side="left", padx=8)

    frame_table = tk.LabelFrame(
        form,
        text=" DANH SÁCH LỚP ",
        font=("Segoe UI", 11, "bold"),
        bg="#F8FAFC"
    )

    frame_table.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    bang = ttk.Treeview(
        frame_table,
        columns=("MaLop", "TenLop"),
        show="headings"
    )

    bang.heading( "MaLop", text="Mã lớp")

    bang.heading("TenLop",text="Tên lớp")

    bang.column("MaLop",width=200,anchor="center")

    bang.column("TenLop",width=600,anchor="w")

    scrollbar = ttk.Scrollbar(
        frame_table,
        orient="vertical",
        command=bang.yview
    )

    bang.configure(
        yscrollcommand=scrollbar.set
    )

    bang.pack(side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    bang.bind(
        "<<TreeviewSelect>>",
        chon_dong
    )
    tai_danh_sach()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mo_form_lop()
    root.mainloop()