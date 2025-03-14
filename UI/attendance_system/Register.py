import tkinter as tk

class Register:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel()
        self.window.title("Register")
        self.window.geometry("1280x800")
        self.window.configure(bg="#2C3E50")

        tk.Label(self.window, text="REGISTER FORM", font=("Arial", 24, "bold"), fg="white", bg="#2C3E50").pack(pady=20)

        self.name_entry = tk.Entry(self.window, font=("Arial", 16), fg="#3498DB", bg="#1B2B40", bd=5, relief="ridge", justify="center")
        self.name_entry.insert(0, "Enter Name")
        self.name_entry.pack(pady=10)

        self.email_entry = tk.Entry(self.window, font=("Arial", 16), fg="#3498DB", bg="#1B2B40", bd=5, relief="ridge", justify="center")
        self.email_entry.insert(0, "Enter Email")
        self.email_entry.pack(pady=10)

        tk.Button(self.window, text="BACK", bg="#E74C3C", fg="white", font=('Arial', 12, 'bold'), height=2, width=15, command=self.go_back).pack(pady=20)

    def go_back(self):
        self.window.destroy()
        self.root.deiconify()
