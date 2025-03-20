import tkinter as tk

root = tk.Tk()
root.title("Face Recognition")
root.geometry("1280x800")




Canvas = tk.Canvas(root,
                   width = 1280,
                   height = 800)
Canvas.pack()
#img = tk.PhotoImage(file = "~/Images/face_recognition.png")


#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Interact with the user

register = tk.Button(root,
                     text = 'Register new user',
                     bg = 'green',
                     fg = 'black',
                     height = 2,
                     width = 20,
                     border = 5 ,
                     font = ('Arial', 14))
register.place(x = 100, y = 500)



take_attendance = tk.Button(root,
                            text = 'Take Attendance',
                            bg = 'green',
                            fg = 'black',
                            height = 2,
                            width = 20,
                            border = 5,
                            font = ('Arial', 14)
                            )
take_attendance.place(x = 500, y = 500)

view_attendance = tk.Button(root,
                            text = 'View Attendance',
                            bg = 'green',
                            fg = 'black',
                            height = 2,
                            width = 20,
                            border = 5,
                            font = ('Arial', 14)
                            )
view_attendance.place(x = 900, y = 500)

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Exit Button
Exit = tk.Button(root, 
                 text = "Exit", 
                 command = root.quit, 
                 border= 5, 
                 bg = 'green', 
                 fg = 'black', 
                 font = ('Arial', 14),
                 height = 1, 
                 width = 20)

Exit.place(x = 500, y = 600)
root.mainloop()
