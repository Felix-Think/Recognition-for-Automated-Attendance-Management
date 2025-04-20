import pymysql

import pymysql

# Kết nối tới MySQL
conn = pymysql.connect(
    host="localhost",
    user="felix",
    password="5812",
    database="NCKH"
)

cursor = conn.cursor()

# 🟢 1. Gọi Stored Procedure để lấy toàn bộ nhân viên
cursor.callproc("Get_Employees")
rows = cursor.fetchall()
print("\n📌 Danh sách nhân viên:")
for row in rows:
    print(row)
