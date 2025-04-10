import cv2
import mediapipe as mp
import numpy as np
import math
from scipy.spatial.transform import Rotation as Rot
# Hàm chuyển đổi ma trận quay thành góc Euler (theo đơn vị độ)
def rotationMatrixToEulerAngles(rotation_matrix):
    rot = Rot.from_matrix(rotation_matrix)
    pitch, yaw, roll = rot.as_euler('xyz', degrees=True)
    if pitch > 90:
        pitch = pitch - 180 
    elif pitch < -90:
        pitch = pitch + 180
    else:
        pitch = pitch
    pitch = -pitch
    return pitch, yaw, roll

# Khởi tạo MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5    ,
    min_tracking_confidence=0.5
)
# Mở camera
cap = cv2.VideoCapture(0)
def DetectFace(cap):
    index =0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Lật khung hình
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Chuyển đổi màu từ BGR sang RGB cho MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Vẽ các điểm landmark
                # for lm in face_landmarks.landmark:
                #     x, y = int(lm.x * w), int(lm.y * h)
                #     cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

                # Chọn các landmark để ước tính head pose:
                # - 1: Mũi (nose tip)
                # - 152: Cằm (chin)
                # - 33: Góc ngoài mắt trái
                # - 263: Góc ngoài mắt phải
                # - 61: Góc miệng trái
                # - 291: Góc miệng phải
                image_points = np.array([
                    (face_landmarks.landmark[1].x * w,   face_landmarks.landmark[1].y * h),    # Nose tip
                    (face_landmarks.landmark[152].x * w, face_landmarks.landmark[152].y * h),  # Chin
                    (face_landmarks.landmark[33].x * w,  face_landmarks.landmark[33].y * h),   # Left eye outer corner
                    (face_landmarks.landmark[263].x * w, face_landmarks.landmark[263].y * h),  # Right eye outer corner
                    (face_landmarks.landmark[61].x * w,  face_landmarks.landmark[61].y * h),   # Left mouth corner
                    (face_landmarks.landmark[291].x * w, face_landmarks.landmark[291].y * h)   # Right mouth corner
                ], dtype="double")

                # Các điểm 3D chuẩn của khuôn mặt (đơn vị mm, giá trị xấp xỉ)
                model_points = np.array([
                    (0.0, 0.0, 0.0),            # Nose tip
                    (0.0, -63.6, -12.5),        # Chin
                    (-43.3, 32.7, -26.0),       # Left eye outer corner
                    (43.3, 32.7, -26.0),        # Right eye outer corner
                    (-28.9, -28.9, -24.1),      # Left Mouth corner
                    (28.9, -28.9, -24.1)        # Right mouth corner
                ])

                # Xây dựng ma trận camera giả định
                focal_length = w  # Ước tính tiêu cự bằng chiều rộng ảnh
                center = (w / 2, h / 2)
                camera_matrix = np.array([
                    [focal_length, 0, center[0]],
                    [0, focal_length, center[1]],
                    [0, 0, 1]
                ], dtype="double")

                # Giả sử không có méo ảnh
                dist_coeffs = np.zeros((4, 1))

                # Tính toán head pose sử dụng hàm solvePnP
                success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
                if success:
                    # Chuyển vector quay thành ma trận quay
                    R, _ = cv2.Rodrigues(rotation_vector)
                    # Tính góc Euler: (pitch, yaw, roll)
                    pitch, yaw, roll = rotationMatrixToEulerAngles(R)

                    # Hiển thị kết quả lên ảnh
                    cv2.putText(frame, f"Pitch: {pitch:.2f}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, f"Yaw: {yaw:.2f}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, f"Roll: {roll:.2f}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                all_points = np.array([[lm.x * w, lm.y * h] for lm in face_landmarks.landmark])
                x_min, y_min = np.min(all_points, axis=0).astype(int)
                x_max, y_max = np.max(all_points, axis=0).astype(int)
                margin = 10  # Thêm biên (margin) nếu cần
                x_min = max(x_min - margin, 0)
                y_min = max(y_min - margin, 0)
                x_max = min(x_max + margin, w)
                y_max = min(y_max + margin, h)
                face_crop = frame[y_min:y_max, x_min:x_max]
                #Thêm range của các pose để chụp tạm thời bấm t để chụp
                key = cv2.waitKey(1) & 0xFF
                if key == ord('t'):
                    cv2.imwrite("cropped_face_"+str(index)+".jpg", face_crop)
                    index+=1
        # Hiển thị khung hình kết quả
        cv2.imshow("MediaPipe Face Mesh - Head Pose Estimation", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
DetectFace(cap)
cap.release()
cv2.destroyAllWindows()
