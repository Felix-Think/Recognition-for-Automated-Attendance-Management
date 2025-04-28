import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='5812',  # Thay bằng password thực tế
        database='NCKH'
    )
    print("Kết nối thành công!")
    with conn.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"Phiên bản MariaDB: {version[0]}")
except pymysql.Error as e:
    print(f"Lỗi kết nối: {e}")
finally:
    if 'conn' in locals():
        conn.close()
