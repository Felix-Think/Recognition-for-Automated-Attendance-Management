import tkinter as tk 
import mysql.connector  # Thay pymysql bằng mysql-connector-python
import time
import cv2
import os
from TakeImage import TakeImage
from PIL import Image, ImageTk
from ViT_Recognition import ViTFaceRecognition
<<<<<<< HEAD
from tkinter import messagebox
=======

>>>>>>> Thinh
class Register:
    def __init__(self, root, main_ui):
        # Kết nối SQL bằng mysql-connector-python
        DB_CONFIG = {
            'host': 'localhost',  # IP của máy bạn
            'user': 'felix',
            'password': '5812',
            'database': 'NCKH',
            'collation': 'utf8mb4_general_ci'
        }
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()

        self.root = tk.Toplevel(root)  # Mở cửa sổ mới thay vì dùng root
        self.main_ui = main_ui  # Lưu lại cửa sổ chính để hiện lại sau này
        self.root.title("Register")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2C3E50")

        # Khi đóng cửa sổ Register, hiện lại Main_UI
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Thanh tiêu đề giả lập
        self.title_bar = tk.Label(self.root, text="REGISTER_EMPLOYEES", bg="#49B0B6", fg="white", font=("Arial", 14, "bold"))
        self.title_bar.pack(fill="x")

        # Khung màu xanh dương #004AAD
        self.img_frame = tk.Frame(self.root, bg="#2C3E50", highlightbackground="#004AAD", highlightthickness=3)
        self.img_frame.place(x=750, y=200, width=300, height=150)

        self.img_label = tk.Label(self.img_frame, image=None, text="MÀU Ô\n#004AAD", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
        self.img_label.pack(expand=True)

        # ID
        self.btn_id = tk.Label(self.root, text="ID", bg="#00E5FF", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_id.place(x=20, y=50)
        self.entry_id = tk.Entry(self.root, font=("Arial", 12, "bold"), width=30)
        self.entry_id.place(x=150, y=50)
        # NAME
        self.btn_name = tk.Label(self.root, text="NAME", bg="#00E5FF", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_name.place(x=20, y=150)
        self.entry_name = tk.Entry(self.root, font=("Arial", 12, "bold"), width=30)
        self.entry_name.place(x=150, y=150)

        # Department 
        self.btn_deparment = tk.Label(self.root, text="DEPARTMENT", bg="#3498DB", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_deparment.place(x=20, y=250)
        self.entry_department = tk.Entry(self.root, font=("Arial", 12, "bold"), width=30)
        self.entry_department.place(x=150, y=250)

        # POSITION
        self.btn_position = tk.Label(self.root, text="POSITION", bg="#3498DB", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_position.place(x=20, y=350)
        self.entry_position = tk.Entry(self.root, font=("Arial", 12, "bold"), width=30)
        self.entry_position.place(x=150, y=350)

        # TAKE IMAGE
        self.take_image = tk.Button(self.root, text="TAKE IMAGE", fg="white", bg="#2C3E50", font=("Arial", 12, "bold"),
                                    width=15, height=2, highlightbackground="#00E5FF", highlightthickness=2, command=self.take_register)
        self.take_image.place(x=650, y=450)
        
        # TRAIN IMAGE
        self.train_image = tk.Button(self.root, text="CONFIRM", fg="white", bg="#2C3E50", font=("Arial", 12, "bold"),
                                     width=15, height=2, highlightbackground="#3498DB", highlightthickness=2, command=self.train_new_user)
        self.train_image.place(x=850, y=450)

    # Back-end main Register

    def get_infor_register(self):
        ID = self.entry_id.get()
        name = self.entry_name.get()
        department = self.entry_department.get()
        position = self.entry_position.get()
        # Get current time   yyyy-mm-dd
        hire_time = time.strftime('%Y-%m-%d')
        return ID, name, department, position, hire_time

    def take_register(self):
        ID, name, department, position, time = self.get_infor_register()
        if not all([ID, name, department, position]):
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        try:
            new_employee = (ID, name, department, position, time)
            self.cursor.callproc("Insert_Employees", new_employee)
            self.conn.commit()
            
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(os.path.join("Datasets", ID), exist_ok=True)
            
            # Mở TakeImage với callback
            self.open_TakeImage(ID)
        except Exception as e:
            messagebox.showerror("Database Error", f"Lỗi: {e}")
    

<<<<<<< HEAD
=======
        self.open_TakeImage(ID)
        # Hien thi anh cuoi cung cua ID
        self.get_img()

>>>>>>> Thinh
    
    def get_img(self):
        img_id = self.entry_id.get()
        img_path = os.path.join("Datasets", img_id)
        
        if not os.path.exists(img_path):
            self.img_label.config(image=None, text="No Image")
            return
            
        try:
            files = sorted([f for f in os.listdir(img_path) if f.endswith(('.jpg', '.png'))])
            if not files:
                self.img_label.config(image=None, text="No Images")
                return
                
            latest_img = files[-1]
            img = Image.open(os.path.join(img_path, latest_img))
            img = img.resize((300, 150), Image.LANCZOS)
            photo_img = ImageTk.PhotoImage(img)
            
            self.img_label.config(image=photo_img)
            self.img_label.image = photo_img
        except Exception as e:
            print(f"Error loading image: {e}")
            self.img_label.config(image=None, text="Load Error")

    def open_TakeImage(self,ID):
        self.root.withdraw() # Ẩn cửa sổ đăng ký
        TakeImage(self.root,ID, callback = self.update_image_after_return) # Mở cửa sổ TakeImage


    def train_new_user(self):
        label = self.entry_id.get()
        src_dir = os.path.join('Datasets', label)
        vit = ViTFaceRecognition(src_dir=src_dir)
        images, labels = vit.load_data(train=False, faiss_index_path='faiss_index.faiss', metadata_path='faiss_index_metadata.pkl')
        #features = vit.extract_features(images)
        #vit.build_and_save_faiss_index(features, save_path='faiss_index') if file is not exist, you have to train index for images
        # add new user
        paths_new_user = os.listdir(src_dir)
        usr_paths = [os.path.join(src_dir, path) for path in paths_new_user] # Lay duong dan de cac anh cua ID 
        vit.add_new_user(usr_paths, label, faiss_index_path='faiss_index.faiss', metadata_path='faiss_index_metadata.pkl')
        print("Đã thêm người dùng mới vào chỉ mục FAISS")

    def update_image_after_return(self):
        """Callback function để cập nhật ảnh sau khi quay lại"""
        self.get_img()
        self.root.deiconify()

    def train_new_user(self, ID):
        label = ID
        src_dir = os.path.join('Datasets', ID)
        vit = ViTFaceRecognition(src_dir=src_dir)
        images, labels = vit.load_data(train=False, faiss_index_path='faiss_index.faiss', metadata_path='faiss_index_metadata.pkl')
        #features = vit.extract_features(images)
        #vit.build_and_save_faiss_index(features, save_path='faiss_index') if file is not exist, you have to train index for images
        # add new user
        paths_new_user = os.listdir(src_dir)
        usr_paths = [os.path.join(src_dir, path) for path in paths_new_user] # Lay duong dan de cac anh cua ID 
        vit.add_new_user(usr_paths, label, faiss_index_path='faiss_index.faiss', metadata_path='faiss_index_metadata.pkl')

    def on_close(self):
        """Handle the window close event."""
        self.main_ui.deiconify()  # Hiện lại Main_UI khi Registe

