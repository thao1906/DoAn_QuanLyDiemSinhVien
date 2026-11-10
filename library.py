import sqlite3

# Them sinh vien
def them_sinh_vien(ma, hoten, gioitinh, ngaysinh, malop):
    conn = sqlite3.connect("QLD.db")
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO SinhVien (MaSV, HoTen, GioiTinh, NgaySinh, MaLop)
        VALUES (?, ?, ?, ?, ?)
        """, (ma, hoten, gioitinh, ngaysinh, malop))

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        conn.close()


# Sua sinh vien
def sua_sinh_vien(ma, hoten, gioitinh, ngaysinh, malop):
    conn = sqlite3.connect("QLD.db")
    cur = conn.cursor()

    cur.execute("""
    UPDATE SinhVien
    SET HoTen=?, GioiTinh=?, NgaySinh=?, MaLop=?
    WHERE MaSV=?
    """, (hoten, gioitinh, ngaysinh, malop, ma))

    conn.commit()
    ket_qua = cur.rowcount
    conn.close()

    return ket_qua > 0


# Xoa sinh vien
def xoa_sinh_vien(ma):
    conn = sqlite3.connect("QLD.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM SinhVien WHERE MaSV=?", (ma,))
    conn.commit()

    ket_qua = cur.rowcount
    conn.close()

    return ket_qua > 0


# Lay danh sach sinh vien
def lay_danh_sach_sinh_vien():
    conn = sqlite3.connect("QLD.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT MaSV, HoTen, GioiTinh, NgaySinh, MaLop
    FROM SinhVien
    ORDER BY MaSV
    """)

    ds = cur.fetchall()
    conn.close()

    return ds


# Tim kiem sinh vien
def tim_sinh_vien(tu_khoa):
    conn = sqlite3.connect("QLD.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT MaSV, HoTen, GioiTinh, NgaySinh, MaLop
    FROM SinhVien
    WHERE MaSV LIKE ? OR HoTen LIKE ?
    ORDER BY MaSV
    """, ("%" + tu_khoa + "%", "%" + tu_khoa + "%"))

    ds = cur.fetchall()
    conn.close()

    return ds