import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import FacePose as FP
class TakeImage:
    def __init__(self, root):
        self.FacePose = FP.FaceEstimator(camera_index=0)
        self.root = tk.Toplevel(root)  # Create a new window
        self.root.title("Take Register")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2C3E50")

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

        # Start Video Capture
        self.cap = self.FacePose.cap
        self.update_video_frame()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_video_frame(self):
        """Update the video frame in the Tkinter window."""
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if ret:    
            # Process the frame using FacePose
            processed_frame = self.FacePose.recognization(frame)
            if processed_frame is None:
                # If no face is detected, use the original frame
                processed_frame = frame

            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to a PIL Image
            img = Image.fromarray(frame_rgb)
            # Convert the PIL Image to an ImageTk object
            imgtk = ImageTk.PhotoImage(image=img)
            # Update the video label with the new frame
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            pitch, yaw, roll = self.FacePose.DetectPose(frame)
            if pitch is not None:
                self.label_pitch.config(text=f"Pitch: {pitch:.2f}")
                self.label_yaw.config(text=f"Yaw: {yaw:.2f}")
                self.label_roll.config(text=f"Roll: {roll:.2f}")
        # Schedule the next frame update
        self.root.after(10, self.update_video_frame)

    def take_image(self):
        """Capture and save an image."""
        ret, frame = self.cap.read()
        frame = self.FacePose.recognization(frame)
        if ret:
            self.FacePose.index += 1
            cv2.imwrite(f"face_{self.FacePose.index}.jpg", frame)
            messagebox.showinfo("Success", "Image captured successfully!")
        else:
            messagebox.showerror("Error", "Failed to capture image.")

    def on_close(self):
        """Handle the window close event."""
        self.cap.release()
        self.root.destroy()
