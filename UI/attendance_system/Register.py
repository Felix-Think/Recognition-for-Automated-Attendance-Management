import tkinter as tk
import pymysql
import time
class Register:
    def __init__(self, root, main_ui):
        #Ket noi SQL
        self.conn = pymysql.connect(host="localhost", user="felix", password="5812", database="NCKH")
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
        self.blue_frame = tk.Frame(self.root, bg="#2C3E50", highlightbackground="#004AAD", highlightthickness=3)
        self.blue_frame.place(x=750, y=200, width=300, height=150)

        self.blue_label = tk.Label(self.blue_frame, text="MÀU Ô\n#004AAD", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
        self.blue_label.pack(expand=True)

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


        
    #def take_attendance(self):
     #   check_insert = self.insert_data()
      #  if check_insert == False:
       #     print("Insert failed'")
        #    # Thong bao loi bang am thanh pptsx3
       # else:
            # Thong bao thanh  va hien camera de chup anh
             
    
    def on_close(self):
        self.main_ui.deiconify()  # Hiện lại Main_UI khi Register đóng
        self.root.destroy()

