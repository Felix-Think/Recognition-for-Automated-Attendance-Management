import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import FaceDetection as FD
from deep_sort_realtime.deepsort_tracker import DeepSort

class Attendance:
    def __init__(self, root):
        self.FaceDetection = FD.FaceDetection(camera_index=0)

        # Initialize DeepSORT tracker
        self.tracker = DeepSort(max_age=30, n_init=3, nn_budget=70)

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
        self.cap = cv2.VideoCapture(0)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_video_frame()

    def update_video_frame(self):
        """Update the video frame in the Tkinter window."""
        ret, frame = self.cap.read()
        if ret:
            # Flip the frame horizontally for a mirrored view
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape  # Get frame dimensions

            # Detect faces using FaceDetection
            detections = self.FaceDetection.detectFaceBoxes(frame)

            # Prepare detections for DeepSORT
            detection_list = []
            for detection in detections:
                x1, y1, x2, y2 = detection
                detection_list.append(([x1, y1, x2 - x1, y2 - y1], 1.0))  # Format: ([x, y, w, h], confidence)

            # Update tracker with detections
            tracks = self.tracker.update_tracks(detection_list, frame=frame)

            # Dictionary to store IN/OUT status for each track_id
            if not hasattr(self, "track_status"):
                self.track_status = {}

            # Draw tracked objects and determine IN/OUT status
            for track in tracks:
                if not track.is_confirmed():
                    continue
                track_id = track.track_id
                ltrb = track.to_ltrb()  # Get bounding box in [left, top, right, bottom] format
                x1, y1, x2, y2 = map(int, ltrb)

                # Determine IN/OUT status
                if track_id not in self.track_status:
                    # First time seeing this track_id
                    if x1 < w / 2:
                        self.track_status[track_id] = "IN"
                    else:
                        self.track_status[track_id] = "OUT"

                # Draw bounding box and track ID with status
                status = self.track_status[track_id]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"ID: {track_id} ({status})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to a PIL Image
            img = Image.fromarray(frame_rgb)

            # Convert the PIL Image to an ImageTk object
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the video label with the new frame
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # Schedule the next frame update
        self.root.after(10, self.update_video_frame)

    def on_close(self):
        """Handle the window close event."""
        self.cap.release()
        self.root.destroy()
