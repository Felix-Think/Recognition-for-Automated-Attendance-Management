import tkinter as tk
import cv2
from PIL import Image, ImageTk
import UI.attendance_system.FacePose as FP

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

        # Video capture frame
        self.video_frame = tk.Frame(self.root, bg="#2C3E50")
        self.video_frame.place(x=50, y=50, width=640, height=480)

        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

        # Start video capture
        self.cap = cv2.VideoCapture(0)  # OpenCV video capture
        self.update_video_frame()

        # Nút màu xanh cyan #00E5FF
        self.btn_cyan_1 = tk.Button(self.root, text="#00E5FF", bg="#00E5FF", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_cyan_1.place(x=150, y=400)

        self.btn_cyan_2 = tk.Button(self.root, text="#00E5FF", bg="#00E5FF", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_cyan_2.place(x=150, y=500)

        # Nút màu xanh dương #3498DB
        self.btn_blue_1 = tk.Button(self.root, text="#3498DB", bg="#3498DB", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_blue_1.place(x=350, y=400)

        self.btn_blue_2 = tk.Button(self.root, text="#3498DB", bg="#3498DB", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
        self.btn_blue_2.place(x=350, y=500)

        # Nút viền xanh cyan
        self.btn_border_cyan = tk.Button(self.root, text="NÚT 2", fg="white", bg="#2C3E50", font=("Arial", 12, "bold"),
                                         width=15, height=2, highlightbackground="#00E5FF", highlightthickness=2)
        self.btn_border_cyan.place(x=650, y=450)

        # Nút viền xanh đậm
        self.btn_border_dark_blue = tk.Button(self.root, text="NÚT 2", fg="white", bg="#2C3E50", font=("Arial", 12, "bold"),
                                              width=15, height=2, highlightbackground="#3498DB", highlightthickness=2)
        self.btn_border_dark_blue.place(x=850, y=450)

    def update_video_frame(self):
        """Update the video frame in the Tkinter window."""
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to a PIL Image
            img = Image.fromarray(frame)
            # Convert the PIL Image to an ImageTk object
            imgtk = ImageTk.PhotoImage(image=img)
            # Update the video label with the new frame
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        # Schedule the next frame update
        self.root.after(10, self.update_video_frame)

    def on_close(self):
        """Handle the window close event."""
        self.cap.release()  # Release the video capture
        self.main_ui.deiconify()  # Hiện lại Main_UI khi Register đóng
        self.root.destroy()
