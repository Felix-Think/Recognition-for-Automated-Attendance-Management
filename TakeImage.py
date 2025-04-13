import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import PoseDetection as FP
import FaceDetection as FD
import os 
import numpy as np
class TakeImage:
    def __init__(self, root,ID, callback = None):
        self.FacePose = FP.PoseDetection()
        self.FaceDetection = FD.FaceDetection(camera_index=0)
        self.preroot = root
        self.root = tk.Toplevel(root)  # Create a new window
        self.root.title("Take Register")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2C3E50")
        self.ID = ID
        self.callback = callback
        self.face = None
        self.face_variation = 0
        # Video Frame
        self.video_frame = tk.Frame(self.root, bg="#2C3E50")
        self.video_frame.place(x=50, y=50, width=640, height=480)
        # Keep the size of video_label fixed
        self.video_label = tk.Label(self.video_frame, width=640, height=480)
        self.video_label.pack()

        # Labels for pitch, yaw, roll
        self.label_pitch = tk.Label(self.root, text="Pitch: N/A", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
        self.label_pitch.place(x=750, y=100)

        self.label_yaw = tk.Label(self.root, text="Yaw: N/A", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
        self.label_yaw.place(x=750, y=150)

        self.label_roll = tk.Label(self.root, text="Roll: N/A", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
        self.label_roll.place(x=750, y=200)

        # Buttons
        self.btn_take_image = tk.Button(self.root, text="Take Image", bg="#3498DB", fg="white", font=("Arial", 12, "bold"),
                                        width=15, height=2, command=self.take_image)
        self.btn_take_image.place(x=750, y=300)
        self.btn_back = tk.Button(self.root, text="Back", bg="#3498DB", fg="white", font=("Arial", 12, "bold"),
                                 width=15, height=2, command=self.on_close)
        self.btn_back.place(x=750, y=400)

        # Start Video Capture
        self.cap = cv2.VideoCapture(0)
        self.update_video_frame()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_video_frame(self):
        """Update the video frame in the Tkinter window."""
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if ret:    
            # Process the frame using FaceDetection
            processed_frame = self.FaceDetection.detectFace(frame)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if len(processed_frame) > 0:
                processed_frame = processed_frame[0]
                face_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                self.face = face_rgb
            else:
                self.face = frame_rgb
            # Convert the frame to a PIL Image
            img = Image.fromarray(frame_rgb)
            # Convert the PIL Image to an ImageTk object
            imgtk = ImageTk.PhotoImage(image=img)
            # Update the video label with the new frame
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            pitch, yaw, roll = self.FacePose.DetectPose(self.face)
            if pitch is not None:
                self.label_pitch.config(text=f"Pitch: {pitch:.2f}")
                self.label_yaw.config(text=f"Yaw: {yaw:.2f}")
                self.label_roll.config(text=f"Roll: {roll:.2f}")
            # if self.face_variation ==0:
            #     if np.abs(pitch) <= 4 and np.abs(yaw) <= 4 and np.abs(roll) <= 4:
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 1:
            #     if (pitch>=3 and pitch <=7) and np.abs(yaw) <= 4 and np.abs(roll) <= 4:
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 2:
            #     if (pitch>=8 and pitch <=12) and np.abs(yaw) <= 4 and np.abs(roll) <= 4:
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 3:  
            #     if (pitch<=-3 and pitch >=-7) and np.abs(yaw) <= 4 and np.abs(roll) <= 4:
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 4:  
            #     if (pitch<=-8 and pitch >=-12) and np.abs(yaw) <= 4 and np.abs(roll) <= 4:
            #         self.face_variation+=1
            #         self.take_image()   
            # elif self.face_variation == 5: 
            #     if abs(pitch)<=4 and (yaw>=3 and yaw <=7)and np.abs(roll) <= 4:
            #         self.face_variation+=1
            #         self.take_image() 
            # elif self.face_variation == 6: 
            #     if abs(pitch)<=4 and (yaw>=8 and yaw <=12)and np.abs(roll) <= 4:
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 7: 
            #     if abs(pitch)<=4 and (yaw<=-3 and yaw >=-7)and np.abs(roll) <= 4:
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 8: 
            #     if abs(pitch)<=4 and (yaw<=-8 and yaw >=-12)and np.abs(roll) <= 4:
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 9: 
            #     if abs(pitch)<=4 and np.abs(yaw) <= 4 and (roll>=3 and roll <=7):
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 10: 
            #     if abs(pitch)<=4 and np.abs(yaw) <= 4 and (roll>=8 and roll <=12):
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 11: 
            #     if abs(pitch)<=4 and np.abs(yaw) <= 4 and (roll<=-3 and roll >=-7):
            #         self.face_variation+=1
            #         self.take_image()
            # elif self.face_variation == 11: 
            #     if abs(pitch)<=4 and np.abs(yaw) <= 4 and (roll<=-8 and roll >=-12):
            #         self.face_variation+=1
            #         self.take_image()
        # Schedule the next frame update
        self.root.after(10, self.update_video_frame)

    def take_image(self):
        """Capture and save an image."""
        face_crop = self.face
        face_crop = cv2.cvtColor(face_crop, cv2.COLOR_RGB2BGR)  # Convert back to BGR for saving
        if face_crop is not None:
            filename = f"face_{self.FaceDetection.index}.png"
            # Tạo folder chứa ảnh, name folder là ID
            path = self.ID
            root = "Datasets"
            root_dir = os.path.join(root, path)
            try:
                if not os.path.exists(root):
                    os.mkdir(root) # root Dataset
                os.mkdir(root_dir) # Dataset/ID for new user
            except FileExistsError:
                pass
            path_file = os.path.join(root_dir, filename)
            cv2.imwrite(path_file, face_crop)
            print(f"Ảnh được lưu: {path_file}")
            self.FaceDetection.index += 1  # Tăng số thứ tự file ảnh

        else:
            messagebox.showerror("Error", "Failed to capture image.")

    def on_close(self):
        """Handle the window close event."""
        self.cap.release()
        self.root.destroy()
        if self.callback:
            self.callback()
        self.preroot.deiconify()

