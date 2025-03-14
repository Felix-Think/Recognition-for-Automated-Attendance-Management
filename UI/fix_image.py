from PIL import Image, ImageOps

# Mở ảnh có nền trong suốt
image = Image.open(r"F:\study\NCKH_2025\Recognition-for-Automated-Attendance-Management\UI\Images\view.png").convert("RGBA")

# Đảo màu ảnh (chuyển đen thành trắng)
inverted_image = ImageOps.invert(image.convert("RGB"))  # Đảo màu
inverted_image.putalpha(image.split()[3])  # Giữ kênh alpha (trong suốt)

# Lưu lại ảnh mới
inverted_image.save("UI/Images/View.png")

# Hiển thị kết quả
inverted_image.show()