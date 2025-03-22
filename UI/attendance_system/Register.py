import tkinter as tk 
import pymysql
import time
import FacePose as FP 
import cv2
import os
from PIL import Image, ImageTk

class Register:
    def __init__(self, root, main_ui):
        #Ket noi SQL
        DB_CONFIG = {
            'host': '192.168.1.6',  # IP của máy bạn
            'user': 'felix',
            'password': '5812',
            'database': 'NCKH'
        }
        self.conn = pymysql.connect(**DB_CONFIG)
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

        # Cửa sổ nhỏ (giả lập)
        #self.window_frame = tk.Frame(self.root, bg="#2C3E50", highlightbackground="white", highlightthickness=2)
        #self.window_frame.place(x=100, y=100, width=400, height=250)

        #self.window_header = tk.Label(self.window_frame, text="#49B0B6", bg="#49B0B6", fg="white", font=("Arial", 12, "bold"))
        #self.window_header.pack(fill="x")

        #self.window_text = tk.Label(self.window_frame, text="BACKGROUND #2C3E50", bg="#2C3E50", fg="black", font=("Arial", 14, "bold"))
        #self.window_text.place(x=100, y=100)

        # Khung màu xanh dương #004AAD
        self.img_frame = tk.Frame(self.root, bg="#2C3E50", highlightbackground="#004AAD", highlightthickness=3)
        self.img_frame.place(x=750, y=200, width=300, height=150)

        self.img_label = tk.Label(self.img_frame, image = None,  text="MÀU Ô\n#004AAD", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
        self.img_label.pack(expand=True)

        # ID
        self.btn_id = tk.Label(self.root, text="ID", bg="#00E5FF", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_id.place(x=20, y=50)
        self.entry_id = tk.Entry(self.root, font=("Arial", 12, "bold"), width=30)
        self.entry_id.place(x=150, y=50)
        #NAME
        self.btn_name = tk.Label(self.root, text="NAME", bg="#00E5FF", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_name.place(x=20, y=150)
        self.entry_name = tk.Entry(self.root, font=("Arial", 12, "bold"), width= 30)
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
                                         width=15, height=2, highlightbackground="#00E5FF", highlightthickness=2, command = self.take_register)
        self.take_image.place(x=650, y=450)
        
        # TRAIN IMAGE
        self.train_image = tk.Button(self.root, text="CONFIRM", fg="white", bg="#2C3E50", font=("Arial", 12, "bold"),
                                              width=15, height=2, highlightbackground="#3498DB", highlightthickness=2)
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
        if not (ID and name and department and position):
            print("Vui lòng nhập đầy đủ thông tin!")
            return
        new_employee = (ID, name, department, position, time)
        try:
            # Insert data to database
            # 🟢 3. Gọi Stored Procedure để chèn nhân viên mới
            self.cursor.callproc("Insert_Employees", new_employee)
            self.conn.commit()

            # check xem co chen duoc khong
            self.cursor.execute("SELECT * FROM Employees WHERE employee_id = %s", (ID,))
            result = self.cursor.fetchone() 
            if result:
                print("Nhan vien da duoc them vao CSDL")
            else:
                print("Them nhan vien that bai")
        except Exception as e:
            print(f"Loi: {e}")

        estimator = FP.FaceEstimator(camera_index=0)
            
        while True:
            ret, frame = estimator.cap.read()
            if not ret:
                break
            
            face_crop = estimator.recognization(frame)  # Nhận diện khuôn mặt
            if face_crop is not None:
                cv2.imshow("Face Crop", face_crop)  # Hiển thị khuôn mặt crop nếu có

            cv2.imshow("Camera", frame)  # Hiển thị camera
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('t'):  # Nhấn 't' để chụp ảnh
                if face_crop is not None:
                    filename = f"face_{estimator.index}.png"
                    #Tao foler chua anh, name folder la ID
                    path = ID
                    root = "Dataset"
                    root_dir = os.path.join(root, path)
                    try:
                        if not os.path.exists(root):
                            os.mkdir(root)
                        os.mkdir(root_dir)
                    except FileExistsError:
                        pass
                    path_file = os.path.join(root_dir, filename)
                    cv2.imwrite(path_file, face_crop)
                    print(f"Ảnh được lưu: {path_file}")
                    estimator.index += 1  # Tăng số thứ tự file ảnh

            elif key == ord('q'):  # Nhấn 'q' để thoát

                break
        estimator.release()
        self.get_img()
    
    def get_img(self):
        img_id = self.entry_id.get()
        img_path = f"Dataset/{img_id}"
        try:
            files = sorted(os.listdir(img_path))
            if not files:
                print("Khong co anh")
                return
            latest_img = files[-1]
            img = Image.open(os.path.join(img_path, latest_img))
            img = img.resize((300, 150))
            img = ImageTk.PhotoImage(img)
            # Hien thi anh len label
            self.img_label.config(image = img) # Hien thi anh len label
            self.img_label.image = img # Giu tham chieu toi anh
        except Exception as e:
            print(f"Loi: {e}")

    def on_close(self):
        """Handle the window close event."""
        self.main_ui.deiconify()  # Hiện lại Main_UI khi Register đóng
        self.root.destroy()


