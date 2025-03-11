import tkinter as tk
from tkinter import Canvas

# Function to open the attendance system
# This function will be called when the user clicks on the "TAKE ATTENDANCE" button
def open_attendance(root):
    root.withdraw() # hide the main window
    attendance = tk.Toplevel() # create a new window
    attendance.title("Attendance System")
    attendance.geometry("1280x800")
    attendance.configure(bg="#1B2B40") # set the background color
    
    id_entry = tk.Entry(attendance, 
                        font=("Arial", 16), 
                        fg="#3498DB", 
                        bg="#1B2B40", 
                        bd=5, 
                        relief="ridge", # set the border style
                        justify="center")
    id_entry.insert(0, "ID") # set the default text
    id_entry.place(x=440, y=150, width=400, height=50) 
    
    
    name_entry = tk.Entry(attendance, 
                          font=("Arial", 16), 
                          fg="#3498DB", 
                          bg="#1B2B40", 
                          bd=5, 
                          relief="ridge", 
                          justify="center")
    name_entry.insert(0, "NAME")
    name_entry.place(x=440, y=230, width=400, height=50)
    
    notification_label = tk.Label(attendance, 
                                  text="NOTIFICATION", 
                                  font=("Arial", 20, "bold"), 
                                  fg="#2ECC71", 
                                  bg="#2C3E50")
    notification_label.place(x=340, y=350, width=600, height=80)
    
    take_image_btn = tk.Button(attendance, 
                               text='TAKE IMAGE', 
                               bg="#3498DB", 
                               fg="white", 
                               font=('Arial', 12, 'bold'), 
                               height=2, 
                               width=15)
    take_image_btn.place(x=300, y=500)
    
    train_image_btn = tk.Button(attendance, 
                                text='TRAIN IMAGE', 
                                bg="#3498DB", 
                                fg="white", 
                                font=('Arial', 12, 'bold'), 
                                height=2, 
                                width=15)
    train_image_btn.place(x=750, y=500)
    
    def go_back():
        attendance.destroy()
        root.deiconify()
    
    back_btn = tk.Button(attendance, 
                         text="BACK", 
                         bg="#E74C3C", 
                         fg="white", 
                         font=('Arial', 12, 'bold'), 
                         height=2, 
                         width=15, 
                         command=go_back)
    back_btn.place(x=530, y=650)

# Function to open the register
# This function will be called when the user clicks on the "REGISTER" button
def open_register(root):
    root.withdraw()
    register = tk.Toplevel()
    register.title("Register")
    register.geometry("1280x800")
    register.configure(bg="#2C3E50")
    
    label = tk.Label(register, 
                     text="REGISTER FORM", 
                     font=("Arial", 24, "bold"), 
                     fg="white", 
                     bg="#2C3E50")
    label.pack(pady=20) 
    
    name_entry = tk.Entry(register, 
                          font=("Arial", 16), 
                          fg="#3498DB", 
                          bg="#1B2B40", 
                          bd=5, 
                          relief="ridge", 
                          justify="center")
    name_entry.insert(0, "Enter Name")
    name_entry.pack(pady=10)
    
    email_entry = tk.Entry(register, 
                           font=("Arial", 16), 
                           fg="#3498DB", 
                           bg="#1B2B40", 
                           bd=5, 
                           relief="ridge", 
                           justify="center")
    email_entry.insert(0, "Enter Email")
    email_entry.pack(pady=10)
    
    def go_back():
        register.destroy()
        root.deiconify()
    
    back_btn = tk.Button(register, 
                         text="BACK", 
                         bg="#E74C3C", 
                         fg="white", 
                         font=('Arial', 12, 'bold'), 
                         height=2, 
                         width=15, 
                         command=go_back)
    back_btn.pack(pady=20)

# Function to create the main window
# This function will be called when the program starts
def create_main():
    root = tk.Tk()
    root.title("Face Recognition Attendance System")
    root.geometry("1280x800")
    root.configure(bg="#2C3E50")
    
    canvas = Canvas(root, 
                    width=1280, 
                    height=800, 
                    bg="#2C3E50", 
                    highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(100, 50, 1180, 100, fill="#0072FF", outline="")
    
    button_style = {
        'bg': "#3498DB", 'fg': "white", 'font': ('Arial', 12, 'bold'),
        'height': 2, 'width': 20, 'borderwidth': 5
    }
    
    register_btn = tk.Button(root, 
                             text='REGISTER', 
                             **button_style, # unpack the dictionary
                             command=lambda: open_register(root)) # call the function when the button is clicked
    register_btn.place(x=200, y=450)
    
    take_attendance_btn = tk.Button(root, 
                                    text='TAKE ATTENDANCE', 
                                    **button_style, 
                                    command=lambda: open_attendance(root))
    take_attendance_btn.place(x=530, y=450)
    
    view_attendance_btn = tk.Button(root, 
                                    text='VIEW ATTENDANCE', 
                                    **button_style)
    view_attendance_btn.place(x=860, y=450)
    
    exit_btn = tk.Button(root, 
                         text="EXIT", 
                         bg="#00FFFF", 
                         fg="black", 
                         font=('Arial', 12, 'bold'), 
                         height=2, 
                         width=20, 
                         borderwidth=5, 
                         command=root.quit)
    exit_btn.place(x=530, y=550)
    
    root.mainloop()

if __name__ == "__main__":
    create_main()
