import tkinter as tk
import pymysql
import time
import cv2
import os
from TakeImage import TakeImage
from PIL import Image, ImageTk
from ViT_Recognition import ViTFaceRecognition
import facebook_vit8s as vits8
from tkinter import messagebox
from functools import partial

class Register:
    def __init__(self, root, main_ui):
        self.root = tk.Toplevel(root)
        self.main_ui = main_ui
        self.model = None
        self.setup_db_connection()
        self.setup_ui()
        self.initialize_face_recognition()

    def setup_db_connection(self):
        """Khởi tạo kết nối database với PyMySQL"""
        DB_CONFIG = {
            'host': 'localhost',
            'user': 'root',
            'password': '5812',
            'database': 'NCKH',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'autocommit': True,
            'client_flag': pymysql.constants.CLIENT.MULTI_STATEMENTS  # Thêm dòng này
        }
        try:
            self.conn = pymysql.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            
            # Đặt collation phù hợp với database
            self.cursor.execute("SET NAMES utf8mb4 COLLATE utf8mb4_0900_ai_ci")
            
            # Test query
            self.cursor.execute("SELECT 1 AS test_connection")
            result = self.cursor.fetchone()
            print("Kết nối database thành công:", result)
        
        except pymysql.Error as err:
            error_msg = f"Lỗi database trong ứng dụng: {err}\n"
            error_msg += f"Thông tin kết nối: {DB_CONFIG}"
            messagebox.showerror("Database Error", error_msg)
            self.root.destroy()
            raise    

    def initialize_face_recognition(self):
        """Khởi tạo model nhận diện khuôn mặt"""
        try:
            self.model = vits8.DinoFaceRecognition(src_dir='train_img/')
            if os.path.exists('faiss_index.faiss'):
                self.model.load_data(
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
            ("FULL NAME", 20, 50),
            ("BIRTHDAY (YYYY-MM-DD)", 20, 100),
            ("GENDER", 20, 150),
            ("DEPARTMENT ID", 20, 200),
            ("POSITION", 20, 250),
            ("WORK STATUS", 20, 300)
        ]
        
        for text, x, y in fields:
            label = tk.Label(self.root, text=text, bg="#00E5FF" if text in ("FULL NAME", "DEPARTMENT ID") else "#3498DB",
                            fg="black", font=("Arial", 12, "bold"), width=20, height=2)
            label.place(x=x, y=y)
            
            if text == "GENDER":
                # Dropdown cho giới tính
                self.entry_gender = tk.StringVar(value="M")
                entry = tk.OptionMenu(self.root, self.entry_gender, "M", "F")
                entry.config(font=("Arial", 12), width=27)
                entry.place(x=170, y=y)
            elif text == "WORK STATUS":
                # Checkbox cho trạng thái làm việc
                self.entry_work_status = tk.BooleanVar(value=True)
                entry = tk.Checkbutton(self.root, variable=self.entry_work_status, text="Active",
                                     font=("Arial", 12), bg="#2C3E50", fg="white", selectcolor="#2C3E50")
                entry.place(x=170, y=y)
            else:
                entry = tk.Entry(self.root, font=("Arial", 12, "bold"), width=30)
                entry.place(x=170, y=y)
                setattr(self, f"entry_{text.lower().replace(' (yyyy-mm-dd)', '').replace(' ', '_')}", entry)

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
        fields = [
            self.entry_full_name.get().strip(),
            self.entry_birthday.get().strip(),
            self.entry_gender.get(),
            self.entry_department_id.get().strip(),
            self.entry_position.get().strip()
        ]
        if not all(fields):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return False
        
        # Kiểm tra định dạng ngày sinh
        try:
            time.strptime(self.entry_birthday.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày sinh phải có định dạng YYYY-MM-DD!")
            return False
            
        # Kiểm tra department_id
        self.cursor.execute("SELECT 1 FROM Department WHERE department_id = %s", 
                          (self.entry_department_id.get(),))
        if not self.cursor.fetchone():
            messagebox.showerror("Lỗi", "Mã phòng ban không tồn tại!")
            return False
            
        return True

    def get_infor_register(self):
        """Lấy thông tin từ form"""
        return (
            self.entry_full_name.get().strip(),
            self.entry_birthday.get().strip(),
            self.entry_gender.get(),
            self.entry_department_id.get().strip(),
            self.entry_position.get().strip(),
            time.strftime('%Y-%m-%d'),  # hire_date
            1 if self.entry_work_status.get() else 0  # work_status
        )

    def take_register(self):
        """Chụp ảnh nhân viên mới"""
        if not self.validate_inputs():
            return
            
        try:
            new_employee = self.get_infor_register()
            
            # Sửa cách gọi stored procedure
            self.cursor.callproc("sp_AddEmployee", [
                new_employee[0],  # full_name
                new_employee[1],  # birthday
                new_employee[2],  # gender
                new_employee[3],  # department_id
                new_employee[4],  # position
                new_employee[5],  # hire_date
                new_employee[6]   # work_status
            ])
            self.conn.commit()
            
            # Lấy employee_id vừa tạo
            self.cursor.execute("""
                SELECT employee_id FROM Employees 
                WHERE full_name = %s AND birthday = %s
                ORDER BY hire_date DESC LIMIT 1
            """, (new_employee[0], new_employee[1]))
            
            emp_id = self.cursor.fetchone()['employee_id']
            
            # Tạo thư mục lưu ảnh
            os.makedirs(os.path.join("Datasets", emp_id), exist_ok=True)
            self.open_TakeImage(emp_id)
            
        except pymysql.Error as err:
            messagebox.showerror("Database Error", 
                f"Lỗi database: {err}\n"
                f"Kiểm tra:\n"
                f"1. Stored procedure sp_AddEmployee có tồn tại?\n"
                f"2. Các tham số có đúng thứ tự?")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Có lỗi xảy ra: {str(e)}")

    def get_img(self):
        """Hiển thị ảnh đại diện"""
        img_id = self.entry_department_id.get().strip()
        if not img_id:
            return
            
        # Sử dụng employee_id thay vì department_id
        self.cursor.execute("SELECT employee_id FROM Employees WHERE department_id = %s LIMIT 1",
                          (img_id,))
        result = self.cursor.fetchone()
        if not result:
            self.img_label.config(image=None, text="CHƯA CÓ ẢNH")
            return
        img_id = result['employee_id']
        
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
            
        # Sử dụng employee_id thay vì department_id
        self.cursor.execute("SELECT employee_id FROM Employees WHERE full_name = %s AND birthday = %s",
                          (self.entry_full_name.get(), self.entry_birthday.get()))
        result = self.cursor.fetchone()
        if not result:
            messagebox.showerror("Lỗi", "Không tìm thấy nhân viên vừa đăng ký!")
            return
        label = result['employee_id']
        
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
                self.model.train(faiss_index_path='faiss_index')
                self.model.add_new_user(
                    usr_paths, 
                    label,
                    faiss_index_path='faiss_index.faiss',
                    metadata_path='faiss_index_metadata.pkl'
                )
            else:
                self.model.add_new_user(
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
