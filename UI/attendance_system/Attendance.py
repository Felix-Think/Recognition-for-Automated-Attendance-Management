import tkinter as tk

class Attendance:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel()
        self.window.title("Attendance System")
        self.window.geometry("1280x800")
        self.window.configure(bg="#1B2B40")

        # Nhập ID
        self.id_entry = tk.Entry(self.window, font=("Arial", 16), fg="#3498DB", bg="#1B2B40", bd=5, relief="ridge", justify="center")
        self.id_entry.insert(0, "ID")
        self.id_entry.place(x=440, y=150, width=400, height=50)

        # Nhập Tên
        self.name_entry = tk.Entry(self.window, font=("Arial", 16), fg="#3498DB", bg="#1B2B40", bd=5, relief="ridge", justify="center")
        self.name_entry.insert(0, "NAME")
        self.name_entry.place(x=440, y=230, width=400, height=50)

        # Label thông báo
        self.notification_label = tk.Label(self.window, text="NOTIFICATION", font=("Arial", 20, "bold"), fg="#2ECC71", bg="#2C3E50")
        self.notification_label.place(x=340, y=350, width=600, height=80)

        # Nút chức năng
        self.create_buttons()

    def create_buttons(self):
        tk.Button(self.window, text='TAKE IMAGE', bg="#3498DB", fg="white", font=('Arial', 12, 'bold'), height=2, width=15).place(x=300, y=500)
        tk.Button(self.window, text='TRAIN IMAGE', bg="#3498DB", fg="white", font=('Arial', 12, 'bold'), height=2, width=15).place(x=750, y=500)

        tk.Button(self.window, text="BACK", bg="#E74C3C", fg="white", font=('Arial', 12, 'bold'), height=2, width=15, command=self.go_back).place(x=530, y=650)

    def go_back(self):
        self.window.destroy()
        self.root.deiconify()