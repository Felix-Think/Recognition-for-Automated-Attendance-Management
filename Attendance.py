import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import FaceDetection as FD
class Attendance:
    def __init__(self, root):
        self.FaceDetection = FD.FaceDetection(camera_index=0)

        self.root = tk.Toplevel(root)  # Create a new window
        self.root.title("Take Register")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2C3E50")
        self.face = None
        # Video Frame
        self.video_frame = tk.Frame(self.root, bg="#2C3E50")
        self.video_frame.place(x=0, y=0, width=1200, height=700)
        # Keep the size of video_label fixed
        self.video_label = tk.Label(self.video_frame, width=1200, height=700)
        self.video_label.pack()
        # Start Video Capture
        self.cap = self.FaceDetection.cap
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_video_frame()
        

    def update_video_frame(self):
        """Update the video frame in the Tkinter window."""
        ret, frame = self.cap.read()
        if ret:
            # Flip the frame horizontally for a mirrored view
            frame = cv2.flip(frame, 1)

            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      
            # Convert the frame to a PIL Image
            img = Image.fromarray(frame_rgb)
            # Convert the PIL Image to an ImageTk object
            imgtk = ImageTk.PhotoImage(image=img)
            # Update the video label with the new frame
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            self.face = self.FaceDetection.detectFace(frame_rgb)
            print(self.face[0].shape)


        # Schedule the next frame update
        self.root.after(10, self.update_video_frame)

    def on_close(self):
        """Handle the window close event."""
        self.cap.release()
        self.root.destroy()
