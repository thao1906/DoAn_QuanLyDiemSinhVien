import sqlite3

conn = sqlite3.connect("QLD.db")
cur = conn.cursor()

cur.execute("""
    SELECT rowid, MaSV, MaMon,
           DiemTX, DiemKT1, DiemKT2,
           DiemKTHP, DiemTB
    FROM Diem
""")

print("DANH SÁCH ĐIỂM HIỆN CÓ:")
for dong in cur.fetchall():
    print(dong)

print("\nSINH VIÊN HIỆN CÓ:")
cur.execute("SELECT * FROM SinhVien")
for dong in cur.fetchall():
    print(dong)

print("\nMÔN HỌC HIỆN CÓ:")
cur.execute("SELECT * FROM MonHoc")
for dong in cur.fetchall():
    print(dong)

conn.close()