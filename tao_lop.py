import sqlite3

conn = sqlite3.connect("QLD.db")
cur = conn.cursor()

cur.execute("""
INSERT OR IGNORE INTO Lop (MaLop, TenLop)
VALUES ('CNTT1', 'Cong nghe thong tin 1')
""")

conn.commit()
conn.close()

print("Da tao lop mau CNTT1")