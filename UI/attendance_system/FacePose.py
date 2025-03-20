import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial.transform import Rotation as Rot

class FaceEstimator:
    def __init__(self, camera_index=0, max_num_faces=1, 
                 detection_confidence=0.5, tracking_confidence=0.5):
        """
        Khởi tạo Estimator:
          - Mở camera (mặc định: camera_index=0)
          - Khởi tạo MediaPipe Face Mesh với các thông số đã cho.
        """
        self.cap = cv2.VideoCapture(camera_index)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.index = 0  # Dùng để đánh số file ảnh khi chụp

    @staticmethod
    def rotationMatrixToEulerAngles(rotation_matrix):
        """
        Chuyển đổi ma trận quay thành góc Euler (đơn vị độ)
        """
        rot = Rot.from_matrix(rotation_matrix)
        pitch, yaw, roll = rot.as_euler('xyz', degrees=True)
        if pitch > 90:
            pitch = pitch - 180 
        elif pitch < -90:
            pitch = pitch + 180
        pitch = -pitch
        return pitch, yaw, roll
    
    def DetectPose(self, frame):
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Chuyển đổi màu từ BGR sang RGB và xử lý với MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Lấy các điểm landmark cần thiết cho ước tính head pose
                image_points = np.array([
                    (face_landmarks.landmark[1].x * w, face_landmarks.landmark[1].y * h),    # Nose tip
                    (face_landmarks.landmark[152].x * w, face_landmarks.landmark[152].y * h),  # Chin
                    (face_landmarks.landmark[33].x * w, face_landmarks.landmark[33].y * h),    # Left eye outer corner
                    (face_landmarks.landmark[263].x * w, face_landmarks.landmark[263].y * h),  # Right eye outer corner
                    (face_landmarks.landmark[61].x * w, face_landmarks.landmark[61].y * h),    # Left mouth corner
                    (face_landmarks.landmark[291].x * w, face_landmarks.landmark[291].y * h)   # Right mouth corner
                ], dtype="double")

                # Các điểm 3D chuẩn của khuôn mặt (đơn vị mm)
                model_points = np.array([
                    (0.0, 0.0, 0.0),            # Nose tip
                    (0.0, -63.6, -12.5),        # Chin
                    (-43.3, 32.7, -26.0),       # Left eye outer corner
                    (43.3, 32.7, -26.0),        # Right eye outer corner
                    (-28.9, -28.9, -24.1),      # Left mouth corner
                    (28.9, -28.9, -24.1)        # Right mouth corner
                ])

                # Xây dựng ma trận camera giả định
                focal_length = w
                center = (w / 2, h / 2)
                camera_matrix = np.array([
                    [focal_length, 0, center[0]],
                    [0, focal_length, center[1]],
                    [0, 0, 1]
                ], dtype="double")

                # Giả sử không có méo ảnh
                dist_coeffs = np.zeros((4, 1))

                # Tính toán head pose sử dụng hàm solvePnP
                success, rotation_vector, translation_vector = cv2.solvePnP(
                    model_points, image_points, camera_matrix, dist_coeffs
                )
                if success:
                    # Chuyển vector quay thành ma trận quay và tính góc Euler
                    R, _ = cv2.Rodrigues(rotation_vector)
                    pitch, yaw, roll = self.rotationMatrixToEulerAngles(R)
    def TakePicture(self, frame):
        """
        Xử lý khung hình:
          - Lật khung hình, chuyển đổi màu cho MediaPipe
          - Xử lý tìm landmark, tính head pose bằng solvePnP
          - Vẽ thông tin head pose lên khung hình
          - Cho phép chụp ảnh khuôn mặt khi nhấn 't'
        """
        # Lật khung hình để tạo cảm giác mirror
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Chuyển đổi màu từ BGR sang RGB và xử lý với MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Lấy các điểm landmark cần thiết cho ước tính head pose
                image_points = np.array([
                    (face_landmarks.landmark[1].x * w, face_landmarks.landmark[1].y * h),    # Nose tip
                    (face_landmarks.landmark[152].x * w, face_landmarks.landmark[152].y * h),  # Chin
                    (face_landmarks.landmark[33].x * w, face_landmarks.landmark[33].y * h),    # Left eye outer corner
                    (face_landmarks.landmark[263].x * w, face_landmarks.landmark[263].y * h),  # Right eye outer corner
                    (face_landmarks.landmark[61].x * w, face_landmarks.landmark[61].y * h),    # Left mouth corner
                    (face_landmarks.landmark[291].x * w, face_landmarks.landmark[291].y * h)   # Right mouth corner
                ], dtype="double")

                # Các điểm 3D chuẩn của khuôn mặt (đơn vị mm)
                model_points = np.array([
                    (0.0, 0.0, 0.0),            # Nose tip
                    (0.0, -63.6, -12.5),        # Chin
                    (-43.3, 32.7, -26.0),       # Left eye outer corner
                    (43.3, 32.7, -26.0),        # Right eye outer corner
                    (-28.9, -28.9, -24.1),      # Left mouth corner
                    (28.9, -28.9, -24.1)        # Right mouth corner
                ])

                # Xây dựng ma trận camera giả định
                focal_length = w
                center = (w / 2, h / 2)
                camera_matrix = np.array([
                    [focal_length, 0, center[0]],
                    [0, focal_length, center[1]],
                    [0, 0, 1]
                ], dtype="double")

                # Tính toán bounding box của khuôn mặt từ tất cả các landmark
                all_points = np.array([[lm.x * w, lm.y * h] for lm in face_landmarks.landmark])
                x_min, y_min = np.min(all_points, axis=0).astype(int)
                x_max, y_max = np.max(all_points, axis=0).astype(int)
                margin = 10
                x_min = max(x_min - margin, 0)
                y_min = max(y_min - margin, 0)
                x_max = min(x_max + margin, w)
                y_max = min(y_max + margin, h)
                face_crop = frame[y_min:y_max, x_min:x_max]
                return face_crop
    
    def recognization(self, frame):
        """
        Xử lý khung hình để lấy khuôn mặt đã crop.
        :param frame: Ảnh đầu vào (BGR) từ OpenCV.
        :return: Ảnh khuôn mặt đã crop, hoặc None nếu không phát hiện được khuôn mặt.
        """
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            # Chỉ lấy khuôn mặt đầu tiên
            face_landmarks = results.multi_face_landmarks[0]
            # Tính bounding box từ tất cả các landmark
            points = np.array([[lm.x * w, lm.y * h] for lm in face_landmarks.landmark])
            x_min, y_min = np.min(points, axis=0).astype(int)
            x_max, y_max = np.max(points, axis=0).astype(int)
            margin = 10  # Thêm biên nếu cần
            x_min = max(x_min - margin, 0)
            y_min = max(y_min - margin, 0)
            x_max = min(x_max + margin, w)
            y_max = min(y_max + margin, h)
            face_crop = frame[y_min:y_max, x_min:x_max]
            return face_crop
        else:
            return None

    def release(self):
        """
        Giải phóng tài nguyên: đóng camera và đóng tất cả các cửa sổ hiển thị.
        """
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    estimator = FaceEstimator(camera_index=0)
    a = estimator.register()
    estimator.release()
