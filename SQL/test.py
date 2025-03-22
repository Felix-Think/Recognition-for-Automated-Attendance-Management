
import pymysql
conn = pymysql.connect(
    host="localhost",
    user="felix",
    password="5812",
    database="NCKH"
)
cursor = conn.cursor()
cursor.callproc("Get_Employees")
rows = cursor.fetchall()
print("\n📌 Danh sách nhân viên:")
for row in rows:
    print(row)
