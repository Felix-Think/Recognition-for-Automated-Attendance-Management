import tkinter as tk

class Register:
    def __init__(self, root, main_ui):
        self.root = tk.Toplevel(root)  # Mở cửa sổ mới thay vì dùng root
        self.main_ui = main_ui  # Lưu lại cửa sổ chính để hiện lại sau này
        self.root.title("Register")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2C3E50")

        # Khi đóng cửa sổ Register, hiện lại Main_UI
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Thanh tiêu đề giả lập
        self.title_bar = tk.Label(self.root, text="#49B0B6", bg="#49B0B6", fg="white", font=("Arial", 14, "bold"))
        self.title_bar.pack(fill="x")

        # Cửa sổ nhỏ (giả lập)
        self.window_frame = tk.Frame(self.root, bg="#2C3E50", highlightbackground="white", highlightthickness=2)
        self.window_frame.place(x=100, y=100, width=400, height=250)

        self.window_header = tk.Label(self.window_frame, text="#49B0B6", bg="#49B0B6", fg="white", font=("Arial", 12, "bold"))
        self.window_header.pack(fill="x")

        self.window_text = tk.Label(self.window_frame, text="BACKGROUND #2C3E50", bg="#2C3E50", fg="black", font=("Arial", 14, "bold"))
        self.window_text.place(x=100, y=100)

        # Khung màu xanh dương #004AAD
        self.blue_frame = tk.Frame(self.root, bg="#2C3E50", highlightbackground="#004AAD", highlightthickness=3)
        self.blue_frame.place(x=750, y=200, width=300, height=150)

        self.blue_label = tk.Label(self.blue_frame, text="MÀU Ô\n#004AAD", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
        self.blue_label.pack(expand=True)

        # Nút màu xanh cyan #00E5FF
        self.btn_cyan_1 = tk.Button(self.root, bg="#00E5FF", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_cyan_1.place(x=150, y=400)

        self.btn_cyan_2 = tk.Button(self.root, bg="#00E5FF", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_cyan_2.place(x=150, y=500)

        # Nút màu xanh dương #3498DB
        self.btn_blue_1 = tk.Button(self.root, bg="#3498DB", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_blue_1.place(x=350, y=400)

        self.btn_blue_2 = tk.Button(self.root, bg="#3498DB", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_blue_2.place(x=350, y=500)

        # Nút viền xanh cyan
        self.btn_border_cyan = tk.Button(self.root, text="NÚT 2", fg="white", bg="#2C3E50", font=("Arial", 12, "bold"),
                                         width=15, height=2, highlightbackground="#00E5FF", highlightthickness=2)
        self.btn_border_cyan.place(x=650, y=450)

        # Nút viền xanh đậm
        self.btn_border_dark_blue = tk.Button(self.root, text="NÚT 2", fg="white", bg="#2C3E50", font=("Arial", 12, "bold"),
                                              width=15, height=2, highlightbackground="#3498DB", highlightthickness=2)
        self.btn_border_dark_blue.place(x=850, y=450)

    def on_close(self):
        self.main_ui.deiconify()  # Hiện lại Main_UI khi Register đóng
        self.root.destroy()
