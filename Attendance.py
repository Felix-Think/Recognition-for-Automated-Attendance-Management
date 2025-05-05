import tkinter as tk
import cv2
from PIL import Image, ImageTk
from deep_sort_realtime.deepsort_tracker import DeepSort
import FaceDetection as FD
import Dino as dino
import time
import numpy as np
import pymysql
import os
from datetime import datetime
from tkinter import messagebox
from FAS import FAS

class Attendance:
    def __init__(self, root, main_ui):
        self.root = tk.Toplevel(root)
        self.main_ui = main_ui
        self.setup_db_connection()
        self.setup_components()
        self.setup_ui()

        # Tracking variables
        self.track_info = {}  # {track_id: {'name': str, 'confidence': float, 'status': str}}
        self.last_recog_time = {}  # {track_id: last_recognition_timestamp}
        self.last_check_in_time = {}  # {employee_id: last_check_in_timestamp}

        # Start video processing
        self.update_video_frame()

    def setup_db_connection(self):
        DB_CONFIG = {
            'host': 'localhost',
            'user': 'root',
            'password': '5812',
            'database': 'NCKH',
            'cursorclass': pymysql.cursors.DictCursor
        } 
        try:
            self.conn = pymysql.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("Kết nối database thành công")
        except pymysql.Error as err:
            messagebox.showerror("Database Error", f"Không thể kết nối database: {err}")
            self.root.destroy()
            raise

    def setup_components(self):
        try:
            self.face_detector = FD.FaceDetection(camera_index=0)
            self.recognizer = dino.DinoFaceRecognition(src_dir = None)
            self.FAS = FAS()
            self.recognizer.load_data(
                faiss_index_path='faiss_index.faiss',
                metadata_path='faiss_index_metadata.pkl'
            )
            self.tracker = DeepSort(
                max_age=30,
                n_init=3,
                nn_budget=70,
                embedder="mobilenet",
                half=True
            )
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise RuntimeError("Could not open video source")
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize: {str(e)}")
            self.root.destroy()

    def setup_ui(self):
        self.root.title("Attendance System")
        self.root.geometry("1280x720")
        self.root.configure(bg="#2C3E50")

        self.video_frame = tk.Frame(self.root, bg="#000000")
        self.video_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(fill="both", expand=True)

        self.control_frame = tk.Frame(self.root, bg="#2C3E50")
        self.control_frame.pack(fill="x", pady=10)

        tk.Button(
            self.control_frame,
            text="Back",
            command=self.on_close,
            bg="#E74C3C",
            fg="white",
            font=("Arial", 12),
            width=15
        ).pack(side="left", padx=20)

    def recognize_face(self, face_img):
        if face_img is None or face_img.size == 0:
            return "Unknown", 0.0
        try:
            rgb_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            results = self.recognizer.recognize_face_topk(rgb_img, top_k=5, threshold=3200)
            return results[0] if results else ("Unknown", 0.0)
        except Exception as e:
            print(f"[ERROR] Face recognition failed: {str(e)}")
            return "Unknown", 0.0

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        face_boxes = self.face_detector.detectFaceBoxes(frame)
        detections = []
        
        for (x1, y1, x2, y2) in face_boxes:
            w, h = x2 - x1, y2 - y1
            detections.append(([x1, y1, w, h], 0.98))

        tracks = self.tracker.update_tracks(detections, frame=frame)

        # Tạo một set để lưu các track_id đã được nhận diện
        processed_tracks = set()

        # Tạo một dictionary để lưu số lần thử tìm kiếm mỗi track_id
        track_attempts = {}

        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id

            # Kiểm tra xem track_id đã được xử lý chưa
            if track_id in processed_tracks:
                continue

            # Kiểm tra số lần thử đã vượt quá giới hạn (10 lần)
            if track_id in track_attempts and track_attempts[track_id] >= 10:
                continue

            x1, y1, x2, y2 = map(int, track.to_ltrb())
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(width, x2), min(height, y2)
            margin_ratio = 0.4
            pad_w = int(w * margin_ratio)
            pad_h = int(h * margin_ratio)

            # Tính box có margin và clamp về trong ảnh
            x1m = max(0, x1 - pad_w)
            y1m = max(0, y1 - pad_h)
            x2m = min(width,  x2 + pad_w)
            y2m = min(height, y2 + pad_h)
            face_w_background = frame[y1m:y2m, x1m:x2m]
            face_roi = frame[y1:y2, x1:x2]

            FAS_score = self.FAS.DetectSpoof(face_w_background)
            if(FAS_score < 0.5):
                continue
            if face_roi.size == 0:
                continue

            current_time = time.time()
            if track_id in self.last_recog_time:
                if current_time - self.last_recog_time[track_id] < 0.5:
                    continue
            self.last_recog_time[track_id] = current_time

            name, confidence = self.recognize_face(face_roi)

            # Cập nhật thông tin track_id nếu chưa có
            if track_id not in self.track_info:
                status = "IN" if x1 < width // 2 else "OUT"
                self.track_info[track_id] = {
                    'name': name,
                    'confidence': confidence,
                    'status': status,
                    'first_seen': current_time,
                    'last_action_time': 0
                }
            else:
                if name != "Unknown":
                    self.track_info[track_id]['name'] = name
                    self.track_info[track_id]['confidence'] = confidence

            # Xử lý attendance nếu nhận diện khuôn mặt thành công
            
            info = self.track_info[track_id]
            if info['name'] != "Unknown" and info['confidence'] < 3200:
                if not info.get('has_checked', False):
                    self.process_attendance(info['name'], info['status'])
                    self.track_info[track_id]['has_checked'] = True
            # Đánh dấu track_id là đã được xử lý
            processed_tracks.add(track_id)

            # Nếu không nhận diện được khuôn mặt, tăng số lần thử
            if name == "Unknown":
                if track_id not in track_attempts:
                    track_attempts[track_id] = 0
                track_attempts[track_id] += 1
            else:
                # Nếu nhận diện thành công, reset số lần thử
                if track_id in track_attempts:
                    track_attempts[track_id] = 0

            # Vẽ thông tin tracking lên frame
            self.draw_tracking_info(frame, track_id, x1, y1, x2, y2)

        return frame


    def process_attendance(self, employee_id, status):
        # Kiểm tra employee_id có tồn tại trong bảng Employees không
        self.cursor.execute("SELECT 1 FROM Employees WHERE employee_id = %s", (employee_id,))
        if not self.cursor.fetchone():
            print(f"[SKIP] Employee ID {employee_id} không tồn tại trong bảng Employees.")
            return
        current_time = time.time()
        if employee_id in self.last_check_in_time:
            if current_time - self.last_check_in_time[employee_id] < 5:
                return
        self.last_check_in_time[employee_id] = current_time

        try:
            today = datetime.now().strftime('%Y-%m-%d')
            attendance_id = f"{employee_id}{datetime.now().strftime('%d%m%y')}"

            self.cursor.execute(
                "SELECT * FROM Attendance WHERE employee_id = %s AND work_date = %s",
                (employee_id, today)
            )
            record = self.cursor.fetchone()
            if not record:
                self.cursor.execute(
                    "INSERT INTO Attendance (attendance_id, employee_id, work_date, check_in_time, status_atd) "
                    "VALUES (%s, %s, %s, NOW(), 1)",
                    (attendance_id, employee_id, today)
                )
                print(f"[CREATE IN] {employee_id}")
            else:
                if record['status_atd'] == 1 and status == "OUT":
                    self.cursor.execute("UPDATE Attendance SET check_out_time = NOW(), status_atd = 0 WHERE attendance_id = %s", (attendance_id,))
                    print(f"[CHECK OUT] {employee_id}")
                elif record['status_atd'] == 0 and status == "IN": 
                    self.cursor.execute(
                        "UPDATE Attendance SET check_in_time = NOW(), status_atd = 1 WHERE attendance_id = %s",
                        (attendance_id,)
                    )
                    print(f"[CHECK BACK IN] {employee_id}")
            self.conn.commit()

        except pymysql.Error as err:
            print(f"Database error during attendance processing: {err}")

    def draw_tracking_info(self, frame, track_id, x1, y1, x2, y2):
        info = self.track_info.get(track_id, {})
        name = info.get('name', "Unknown")
        confidence = info.get('confidence', 0)
        status = info.get('status', "IN")
        box_color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        text_color = (255, 255, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
        display_text = [
            f"ID: {name}",
            f"Conf: {confidence:.2f}" if name != "Unknown" else "",
            f"Status: {status}"
        ]

        y_offset = y1 - 35
        for i, text in enumerate(filter(None, display_text)):
            cv2.putText(
                frame,
                text,
                (x1, max(y_offset + i*20, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                text_color,
                1,
                cv2.LINE_AA
            )

    def update_video_frame(self):
        ret, frame = self.cap.read()
        if ret:
            processed_frame = self.process_frame(frame)
            rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)
        self.root.after(10, self.update_video_frame)

    def on_close(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()
        self.root.destroy()
        self.main_ui.deiconify()

    def __del__(self):
        self.on_close()
