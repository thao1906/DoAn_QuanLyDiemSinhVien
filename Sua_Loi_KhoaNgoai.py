import sqlite3

conn = sqlite3.connect("QLD.db")
cur = conn.cursor()

try:
    cur.execute("DELETE FROM Diem WHERE rowid IN (2, 3, 4, 5)")

    conn.commit()

    print("Đã xóa 4 dòng điểm bị lỗi!")

    cur.execute("PRAGMA foreign_key_check")
    loi = cur.fetchall()

    if not loi:
        print("Không còn lỗi khóa ngoại!")
    else:
        print("Vẫn còn lỗi:", loi)

except sqlite3.Error as e:
    conn.rollback()
    print("Lỗi:", e)

finally:
    conn.close()