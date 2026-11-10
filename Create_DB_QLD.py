import sqlite3

# Ket noi co so du lieu
conn = sqlite3.connect("QLD.db")
cur = conn.cursor()

# Tao bang Lop
cur.execute("""
CREATE TABLE IF NOT EXISTS Lop (
    MaLop TEXT PRIMARY KEY,
    TenLop TEXT NOT NULL
)
""")

# Tao bang SinhVien
cur.execute("""
CREATE TABLE IF NOT EXISTS SinhVien (
    MaSV TEXT PRIMARY KEY,
    HoTen TEXT NOT NULL,
    GioiTinh TEXT,
    NgaySinh TEXT,
    MaLop TEXT,
    FOREIGN KEY (MaLop) REFERENCES Lop(MaLop)
)
""")

# Tao bang MonHoc
cur.execute("""
CREATE TABLE IF NOT EXISTS MonHoc (
    MaMon TEXT PRIMARY KEY,
    TenMon TEXT NOT NULL
)
""")

# Tao bang Diem

cur.execute("""
CREATE TABLE IF NOT EXISTS Diem (
    MaSV TEXT,
    MaMon TEXT,
    DiemTX REAL CHECK (DiemTX >= 0 AND DiemTX <= 10),
    DiemKT1 REAL CHECK (DiemKT1 >= 0 AND DiemKT1 <= 10),
    DiemKT2 REAL CHECK (DiemKT2 >= 0 AND DiemKT2 <= 10),
    DiemKTHP REAL CHECK (DiemKTHP >= 0 AND DiemKTHP <= 10),
    DiemTB REAL CHECK (DiemTB >= 0 AND DiemTB <= 10),
    PRIMARY KEY (MaSV, MaMon),
    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV),
    FOREIGN KEY (MaMon) REFERENCES MonHoc(MaMon)
)
""")


# Luu du lieu va dong ket noi
#conn.commit()
#conn.close()

#print("Tao co so du lieu QLD.db thanh cong!")


# Cap nhat cac cot diem neu chua co
cur.execute("PRAGMA table_info(Diem)")
cac_cot = [dong[1] for dong in cur.fetchall()]

cac_cot_moi = [
    ("DiemTX", "REAL"),
    ("DiemKT1", "REAL"),
    ("DiemKT2", "REAL"),
    ("DiemKTHP", "REAL"),
    ("DiemTB", "REAL")
]

for ten_cot, kieu_du_lieu in cac_cot_moi:
    if ten_cot not in cac_cot:
        cur.execute(
            f"ALTER TABLE Diem ADD COLUMN {ten_cot} {kieu_du_lieu}"
        )
        print("Da them cot:", ten_cot)

conn.commit()
conn.close()

print("Cap nhat co so du lieu thanh cong!")
