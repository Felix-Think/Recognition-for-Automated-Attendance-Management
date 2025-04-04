#Chạy ứng dụng chính
import tkinter as tk
from Main_UI import Main_UI

if __name__ == "__main__":
    root = tk.Tk()
    app = Main_UI(root)
    root.mainloop() 
    