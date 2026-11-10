import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


def ket_noi():
    return sqlite3.connect("QLD.db")


def lay_danh_sach():
    for item in bang.get_children():
        bang.delete(item)

    conn = ket_noi()
    cur = conn.cursor()
    cur.execute("SELECT MaMon, TenMon FROM MonHoc")

    for dong in cur.fetchall():
        bang.insert("", "end", values=dong)

    conn.close()


def lam_moi():
    txtMaMon.delete(0, tk.END)
    txtTenMon.delete(0, tk.END)


def chon_mon(event):
    dong = bang.focus()

    if dong:
        du_lieu = bang.item(dong, "values")
        lam_moi()
        txtMaMon.insert(0, du_lieu[0])
        txtTenMon.insert(0, du_lieu[1])


def them_mon():
    ma = txtMaMon.get().strip()
    ten = txtTenMon.get().strip()

    if ma == "" or ten == "":
        messagebox.showwarning("Thông báo", "Hãy nhập đầy đủ thông tin!",parent=txtMaMon.winfo_toplevel())
        return

    conn = ket_noi()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO MonHoc (MaMon, TenMon) VALUES (?, ?)",
            (ma, ten)
        )
        conn.commit()
        messagebox.showinfo("Thông báo", "Thêm môn học thành công!",parent=txtMaMon.winfo_toplevel())
        lam_moi()
        lay_danh_sach()
    except sqlite3.IntegrityError:
        messagebox.showerror("Lỗi", "Mã môn đã tồn tại!")
    finally:
        conn.close()


def sua_mon():
    ma = txtMaMon.get().strip()
    ten = txtTenMon.get().strip()

    if ma == "" or ten == "":
        messagebox.showwarning("Thông báo", "Hãy chọn môn học và nhập tên mới!",parent=txtMaMon.winfo_toplevel())
        return

    conn = ket_noi()
    cur = conn.cursor()
    cur.execute(
        "UPDATE MonHoc SET TenMon=? WHERE MaMon=?",
        (ten, ma)
    )
    conn.commit()
    so_dong = cur.rowcount
    conn.close()

    if so_dong > 0:
        messagebox.showinfo("Thông báo", "Sửa môn học thành công!",parent=txtMaMon.winfo_toplevel())
        lam_moi()
        lay_danh_sach()
    else:
        messagebox.showwarning("Thông báo", "Không tìm thấy mã môn!")


def xoa_mon():
    ma = txtMaMon.get().strip()

    if ma == "":
        messagebox.showwarning("Thông báo", "Hãy chọn môn học cần xóa!",parent=txtMaMon.winfo_toplevel())
        return

    if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa môn học này?",parent=txtMaMon.winfo_toplevel()):
        return

    conn = ket_noi()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM MonHoc WHERE MaMon=?", (ma,))
        conn.commit()

        if cur.rowcount > 0:
            messagebox.showinfo("Thông báo", "Xóa môn học thành công!",parent=txtMaMon.winfo_toplevel())
        else:
            messagebox.showwarning("Thông báo", "Không tìm thấy mã môn!")

        lam_moi()
        lay_danh_sach()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Lỗi", "Môn học đang được sử dụng trong bảng điểm, không thể xóa!"
        )
    finally:
        conn.close()


def mo_form_mon_hoc():
    global txtMaMon, txtTenMon, bang

    form = tk.Toplevel()
    form.title("QUẢN LÝ MÔN HỌC")
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
    text="THÔNG TIN MÔN HỌC",
    font=("Segoe UI", 12, "bold"),
    fg="#000000",
    bg="white",
    padx=20,
    pady=15
)

    frame_input.pack(
        fill="x",
        padx=15,
        pady=(20, 10)
    )

    # Khung giữa
    khung_nhap = tk.Frame(
        frame_input,
        bg="white"
    )

    khung_nhap.pack()

    tk.Label(
        khung_nhap,
        text="Mã môn",
        bg="white",
        font=("Segoe UI", 10)
    ).grid(
        row=0,
        column=0,
        padx=(20, 10),
        pady=10
    )

    txtMaMon = ttk.Entry(
        khung_nhap,
        width=25
    )

    txtMaMon.grid(
        row=0,
        column=1,
        padx=(0, 30)
    )

    tk.Label(
        khung_nhap,
        text="Tên môn",
        bg="white",
        font=("Segoe UI", 10)
    ).grid(
        row=0,
        column=2,
        padx=(0, 10),
        pady=10
    )

    txtTenMon = ttk.Entry(
        khung_nhap,
        width=40
    )

    txtTenMon.grid(
        row=0,
        column=3,
        padx=(0, 20)
    )

    frame_btn = tk.Frame(form,bg="#F8FAFC")

    frame_btn.pack(fill="x",pady=10)

    btn_container = tk.Frame(frame_btn,bg="#F8FAFC")

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

    tao_nut("➕ Thêm",them_mon,"#16A34A").pack(side="left", padx=8)

    tao_nut("✏️ Sửa",sua_mon,"#2563EB").pack(side="left", padx=8)

    tao_nut("🗑 Xóa",xoa_mon, "#DC2626").pack(side="left", padx=8)

    tao_nut("🔄 Làm mới",lam_moi, "#64748B" ).pack(side="left", padx=8)

    frame_table = tk.LabelFrame(
        form,
        text=" DANH SÁCH MÔN HỌC ",
        font=("Segoe UI", 11, "bold"),
        bg="#F8FAFC"
    )

    frame_table.pack(fill="both",expand=True,padx=15,pady=10)

    bang = ttk.Treeview(frame_table,columns=("MaMon", "TenMon"),show="headings")

    bang.heading("MaMon",text="Mã môn")

    bang.heading("TenMon",text="Tên môn học")

    bang.column("MaMon",width=180,anchor="center")

    bang.column("TenMon",width=600,anchor="w")

    scrollbar = ttk.Scrollbar(frame_table,orient="vertical",command=bang.yview)

    bang.configure( yscrollcommand=scrollbar.set)

    bang.pack(side="left", fill="both", expand=True)

    scrollbar.pack(side="right",fill="y")

    bang.bind(
        "<<TreeviewSelect>>",
        chon_mon
    )

    lay_danh_sach()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mo_form_mon_hoc()
    root.mainloop()