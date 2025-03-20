import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from Attendance import Attendance
from Register import Register

class Main_UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1280x800")
        self.root.configure(bg="#2C3E50")

        # Canvas for decoration
        self.canvas = Canvas(root, width=1280, height=800, bg="#2C3E50", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_rectangle(100, 50, 1180, 100, fill="#0072FF", outline="")

        # Load images
        self.register_image = self.load_img(r"../Images/register.png", (200, 300))
        self.attendance_image = self.load_img(r"../Images/attendance.png", (200, 300))
        self.view_image = self.load_img(r"../Images/view.png", (250, 250))

        # Create buttons with images
        self.create_buttons()

    def load_img(self, path, size):
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def create_buttons(self):
        button_style = {
            'bg': "#3498DB", 'fg': "white", 'font': ('Arial', 12, 'bold'),
            'height': 2, 'width': 20, 'borderwidth': 5
        }

        # Register button and image
        Register_logo = tk.Label(self.root, image=self.register_image, bg="#2C3E50")
        Register_logo.place(relx=0.2, rely=0.45, anchor='center')

        Register_bt = tk.Button(self.root, 
                    text='REGISTER', 
                    **button_style, 
                    command=self.open_register
                    )
        Register_bt.place(relx=0.2, rely=0.7, anchor='center')
        
        # Take Attendance button and image
        Attendance_logo = tk.Label(self.root, image=self.attendance_image, bg="#2C3E50")
        Attendance_logo.place(relx=0.5, rely=0.45, anchor='center')

        Attendance_bt = tk.Button(self.root, 
                        text='TAKE ATTENDANCE', 
                        **button_style, 
                        command=self.open_attendance
                        )
        Attendance_bt.place(relx=0.5, rely=0.7, anchor='center')
        
        # View Attendance button and image
        View_Logo = tk.Label(self.root, image=self.view_image, bg="#2C3E50")
        View_Logo.place(relx=0.8, rely=0.45, anchor='center')

        View_bt = tk.Button(self.root, 
                  text='VIEW ATTENDANCE', 
                  **button_style
                  )
        View_bt.place(relx=0.8, rely=0.7, anchor='center')
        
        # Exit button
        Exit_bt = tk.Button(self.root, 
                  text="EXIT", 
                  bg="#00FFFF", 
                  fg="black", 
                  font=('Arial', 12, 'bold'), 
                  height=2, 
                  width=20, 
                  borderwidth=5, 
                  command=self.root.quit
                  )
        Exit_bt.place(relx=0.5, rely=0.9, anchor='center')

    def open_attendance(self):
        self.root.withdraw()
        Attendance(self.root)

    def open_register(self):
        self.root.withdraw()
        Register(self.root, self.root)
