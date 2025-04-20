import tkinter as tk
import cv2
from PIL import Image, ImageTk
from deep_sort_realtime.deepsort_tracker import DeepSort
import FaceDetection as FD
import ViT_Recognition as ViT
import time
import numpy as np

class Attendance:
    def __init__(self, root, main_ui):
        self.root = tk.Toplevel(root)
        self.main_ui = main_ui
        self.setup_components()
        self.setup_ui()
        
        # Tracking variables
        self.track_info = {}  # {track_id: {'name': str, 'confidence': float, 'status': str}}
        self.last_recog_time = {}  # {track_id: last_recognition_timestamp}
        
        # Start video processing
        self.update_video_frame()
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.root.title("Attendance System")
        self.root.geometry("1280x720")
        self.root.configure(bg="#2C3E50")
        
        # Video display
        self.video_frame = tk.Frame(self.root, bg="#000000")
        self.video_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(fill="both", expand=True)
        
        # Control panel
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
    def setup_components(self):
        """Khởi tạo các thành phần hệ thống"""
        try:
            # Face detection
            self.face_detector = FD.FaceDetection(camera_index=0)
            
            # Face recognition - CHỈ SỬ DỤNG recognize_face
            self.recognizer = ViT.ViTFaceRecognition()
            self.recognizer.load_data(
                faiss_index_path='faiss_index.faiss',
                metadata_path='faiss_index_metadata.pkl'
            )
            
            # Object tracker
            self.tracker = DeepSort(
                max_age=30,
                n_init=3,
                nn_budget=70,
                embedder="mobilenet",
                half=True
            )
            
            # Video capture
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise RuntimeError("Could not open video source")
                
        except Exception as e:
            tk.messagebox.showerror("Initialization Error", f"Failed to initialize: {str(e)}")
            self.root.destroy()

    def recognize_face(self, face_img):
        """
        Nhận diện khuôn mặt sử dụng ĐÚNG PHƯƠNG THỨC recognize_face của ViT
        
        Args:
            face_img: numpy.ndarray - Ảnh khuôn mặt (BGR format)
            
        Returns:
            Tuple (user_name, confidence) hoặc ("Unknown", 0.0) nếu lỗi
        """
        if face_img is None or face_img.size == 0:
            return "Unknown", 0.0
            
        try:
            # Chuyển đổi sang RGB
            rgb_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            
            # Gọi ĐÚNG phương thức recognize_face
            results = self.recognizer.recognize_face(rgb_img, threshold = 0.7)
            
            # Kết quả trả về là list[(user_name, confidence)]
            if results and len(results) > 0:
                return results[0]  # Lấy kết quả đầu tiên
            return "Unknown", 0.0
            
        except Exception as e:
            print(f"[ERROR] Face recognition failed: {str(e)}")
            return "Unknown", 0.0

    def process_frame(self, frame):
        """Xử lý từng frame video"""
        # Mirror effect
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        
        # Phát hiện khuôn mặt
        face_boxes = self.face_detector.detectFaceBoxes(frame)
        
        # Chuẩn bị dữ liệu cho DeepSort
        detections = []
        for (x1, y1, x2, y2) in face_boxes:
            w, h = x2 - x1, y2 - y1
            detections.append(([x1, y1, w, h], 0.95))  # (bbox, confidence)
        
        # Cập nhật tracker
        tracks = self.tracker.update_tracks(detections, frame=frame)
        
        # Xử lý từng track
        for track in tracks:
            if not track.is_confirmed():
                continue
                
            track_id = track.track_id
            x1, y1, x2, y2 = map(int, track.to_ltrb())
            
            # Đảm bảo tọa độ hợp lệ
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(width, x2), min(height, y2)
            
            # Trích xuất vùng khuôn mặt
            face_roi = frame[y1:y2, x1:x2]
            if face_roi.size == 0:
                continue
                
            # Giới hạn tần suất nhận diện (1 lần/giây cho mỗi track)
            current_time = time.time()
            if track_id in self.last_recog_time:
                if current_time - self.last_recog_time[track_id] < 0.2:
                    continue
            self.last_recog_time[track_id] = current_time
            
            # Nhận diện khuôn mặt - CHỈ SỬ DỤNG recognize_face
            name, confidence = self.recognize_face(face_roi)
            
            # Cập nhật thông tin track
            if track_id not in self.track_info:
                self.track_info[track_id] = {
                    'name': name,
                    'confidence': confidence,
                    'status': "IN" if x1 < width//2 else "OUT",
                    'first_seen': current_time
                }
            else:
                self.track_info[track_id].update({
                    'name': name,
                    'confidence': confidence
                })
            
            # Vẽ thông tin lên frame
            self.draw_tracking_info(frame, track_id, x1, y1, x2, y2)
        
        return frame

    def draw_tracking_info(self, frame, track_id, x1, y1, x2, y2):
        """Vẽ bounding box và thông tin nhận diện"""
        info = self.track_info.get(track_id, {})
        name = info.get('name', "Unknown")
        confidence = info.get('confidence', 0)
        status = info.get('status', "IN")
        
        # Màu sắc tùy thuộc vào trạng thái nhận diện
        box_color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        text_color = (255, 255, 255)
        
        # Vẽ bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
        
        # Chuẩn bị thông tin hiển thị
        display_text = [
            f"Name: {name}",
            f"Conf: {confidence:.2f}" if name != "Unknown" else "",
            f"Status: {status}"
        ]
        
        # Vẽ từng dòng text
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

    # Các phương thức update_video_frame, on_close, __del__ giữ nguyên như trước
    def update_video_frame(self):
        """Cập nhật video frame lên giao diện"""
        ret, frame = self.cap.read()
        
        if ret:
            processed_frame = self.process_frame(frame)
            
            # Chuyển đổi định dạng hình ảnh
            rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Cập nhật giao diện
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)
        
        # Lặp lại sau 10ms
        self.root.after(10, self.update_video_frame)

    def __del__(self):
        """Giải phóng tài nguyên"""
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
    def on_close(self):
        """Xử lý khi đóng cửa sổ hoặc ấn Back"""
        # Giải phóng camera nếu có
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        
        self.root.destroy()
        self.main_ui.deiconify()
