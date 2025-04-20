import tkinter as tk
import mysql.connector
import time
import cv2
import os
from TakeImage import TakeImage
from PIL import Image, ImageTk
from ViT_Recognition import ViTFaceRecognition
from tkinter import messagebox
from functools import partial

class Register:
    def __init__(self, root, main_ui):
        self.root = tk.Toplevel(root)
        self.main_ui = main_ui
        self.vit = None  # Thêm biến vit ở mức class
        self.setup_db_connection()
        self.setup_ui()
        self.initialize_face_recognition()

    def setup_db_connection(self):
        """Khởi tạo kết nối database"""
        DB_CONFIG = {
            'host': 'localhost',
            'user': 'felix',
            'password': '5812',
            'database': 'NCKH',
            'collation': 'utf8mb4_general_ci'
        }
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Kết nối database thất bại: {err}")
            self.root.destroy()

    def initialize_face_recognition(self):
        """Khởi tạo model nhận diện khuôn mặt"""
        try:
            self.vit = ViTFaceRecognition(src_dir=None)
            if os.path.exists('faiss_index.faiss'):
                self.vit.load_data(
                    faiss_index_path='faiss_index.faiss',
                    metadata_path='faiss_index_metadata.pkl'
                )
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể khởi tạo model nhận diện: {e}")

    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.root.title("Register")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2C3E50")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Title bar
        self.title_bar = tk.Label(self.root, text="REGISTER_EMPLOYEES", bg="#49B0B6", 
                                fg="white", font=("Arial", 14, "bold"))
        self.title_bar.pack(fill="x")

        # Image preview frame
        self.img_frame = tk.Frame(self.root, bg="#2C3E50", 
                                highlightbackground="#004AAD", highlightthickness=3)
        self.img_frame.place(x=750, y=200, width=300, height=150)
        self.img_label = tk.Label(self.img_frame, image=None, text="ẢNH ĐẠI DIỆN", 
                                bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
        self.img_label.pack(expand=True)

        # Form fields
        fields = [
            ("ID", 20, 50),
            ("NAME", 20, 150),
            ("DEPARTMENT", 20, 250),
            ("POSITION", 20, 350)
        ]
        
        for text, x, y in fields:
            label = tk.Label(self.root, text=text, bg="#00E5FF" if text in ("ID", "NAME") else "#3498DB",
                            fg="black", font=("Arial", 12, "bold"), width=15, height=2)
            label.place(x=x, y=y)
            
            entry = tk.Entry(self.root, font=("Arial", 12, "bold"), width=30)
            entry.place(x=150, y=y)
            setattr(self, f"entry_{text.lower()}", entry)

        # Buttons
        buttons = [
            ("TAKE IMAGE", "#00E5FF", self.take_register, 650, 450),
            ("CONFIRM", "#3498DB", self.train_new_user, 850, 450),
            ("BACK", "#3498DB", self.on_close, 650, 550)
        ]
        
        for text, color, command, x, y in buttons:
            btn = tk.Button(self.root, text=text, fg="white", bg="#2C3E50", 
                          font=("Arial", 12, "bold"), width=15, height=2,
                          highlightbackground=color, highlightthickness=2, 
                          command=command)
            btn.place(x=x, y=y)

    def validate_inputs(self):
        """Kiểm tra các trường input"""
        if not all([
            self.entry_id.get().strip(),
            self.entry_name.get().strip(),
            self.entry_department.get().strip(),
            self.entry_position.get().strip()
        ]):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return False
        return True

    def get_infor_register(self):
        """Lấy thông tin từ form"""
        return (
            self.entry_id.get().strip(),
            self.entry_name.get().strip(),
            self.entry_department.get().strip(),
            self.entry_position.get().strip(),
            time.strftime('%Y-%m-%d')
        )

    def take_register(self):
        """Chụp ảnh nhân viên mới"""
        if not self.validate_inputs():
            return
            
        try:
            new_employee = self.get_infor_register()
            self.cursor.callproc("Insert_Employees", new_employee)
            self.conn.commit()
            
            # Tạo thư mục lưu ảnh
            os.makedirs(os.path.join("Datasets", new_employee[0]), exist_ok=True)
            self.open_TakeImage(new_employee[0])
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Lỗi database: {err}")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Có lỗi xảy ra: {e}")

    def get_img(self):
        """Hiển thị ảnh đại diện"""
        img_id = self.entry_id.get().strip()
        if not img_id:
            return
            
        img_path = os.path.join("Datasets", img_id)
        
        try:
            if not os.path.exists(img_path):
                self.img_label.config(image=None, text="CHƯA CÓ ẢNH")
                return
                
            files = sorted([f for f in os.listdir(img_path) if f.lower().endswith(('.jpg', '.png'))])
            if not files:
                self.img_label.config(image=None, text="KHÔNG TÌM THẤY ẢNH")
                return
                
            latest_img = files[-1]
            img = Image.open(os.path.join(img_path, latest_img))
            img = img.resize((300, 150), Image.LANCZOS)
            photo_img = ImageTk.PhotoImage(img)
            
            self.img_label.config(image=photo_img)
            self.img_label.image = photo_img
        except Exception as e:
            print(f"Error loading image: {e}")
            self.img_label.config(image=None, text="LỖI TẢI ẢNH")

    def open_TakeImage(self, emp_id):
        """Mở cửa sổ chụp ảnh"""
        self.root.withdraw()
        TakeImage(
            self.root,
            emp_id,
            callback=self.update_image_after_return
        )

    def train_new_user(self):
        """Thêm nhân viên mới vào hệ thống nhận diện"""
        if not self.validate_inputs():
            return
            
        label = self.entry_id.get().strip()
        src_dir = os.path.join('Datasets', label)
        
        try:
            if not os.path.exists(src_dir):
                messagebox.showerror("Lỗi", f"Không tìm thấy thư mục ảnh cho {label}")
                return
                
            valid_exts = ('.png', '.jpg', '.jpeg')
            usr_paths = [
                os.path.join(src_dir, f) for f in os.listdir(src_dir) 
                if f.lower().endswith(valid_exts)
            ]
            
            if not usr_paths:
                messagebox.showerror("Lỗi", f"Không có ảnh hợp lệ trong thư mục {label}")
                return
                
            # Thêm vào hệ thống nhận diện
            if not os.path.exists('faiss_index.faiss'):
                self.vit.train(faiss_index_path='faiss_index')
            else:
                self.vit.add_new_user(
                    usr_paths, 
                    label,
                    faiss_index_path='faiss_index.faiss',
                    metadata_path='faiss_index_metadata.pkl'
                )
            
            messagebox.showinfo("Thành công", f"Đã đăng ký thành công nhân viên {label}")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Có lỗi khi đăng ký: {e}")

    def update_image_after_return(self):
        """Callback sau khi chụp ảnh xong"""
        self.get_img()
        self.root.deiconify()

    def on_close(self):
        """Xử lý khi đóng cửa sổ"""
        try:
            if hasattr(self, 'cursor'):
                self.cursor.close()
            if hasattr(self, 'conn'):
                self.conn.close()
        except Exception as e:
            print(f"Error closing resources: {e}")
            
        self.root.destroy()
        self.main_ui.deiconify()
