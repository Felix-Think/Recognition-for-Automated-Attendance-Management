import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial.transform import Rotation as Rot

class PoseDetection:
    def __init__(self, max_num_faces=1, 
                 detection_confidence=0.5, tracking_confidence=0.5):
        """
        Khởi tạo Estimator:
          - Khởi tạo MediaPipe Face Mesh với các thông số đã cho.
        """
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

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
        """
        Detects the head pose from the given frame using MediaPipe Face Mesh.
        :param frame: Input frame (BGR) from OpenCV.
        :return: Tuple (pitch, yaw, roll) in degrees, or (0, 0, 0) if no face is detected.
        """
        h, w, _ = frame.shape

        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            return -200, -200, -200  # No face detected

        # Process the first detected face
        face_landmarks = results.multi_face_landmarks[0]

        # Extract 2D image points for head pose estimation
        try:
            image_points = np.array([
                (face_landmarks.landmark[1].x * w, face_landmarks.landmark[1].y * h),    # Nose tip
                (face_landmarks.landmark[152].x * w, face_landmarks.landmark[152].y * h),  # Chin
                (face_landmarks.landmark[33].x * w, face_landmarks.landmark[33].y * h),    # Left eye outer corner
                (face_landmarks.landmark[263].x * w, face_landmarks.landmark[263].y * h),  # Right eye outer corner
                (face_landmarks.landmark[61].x * w, face_landmarks.landmark[61].y * h),    # Left mouth corner
                (face_landmarks.landmark[291].x * w, face_landmarks.landmark[291].y * h)   # Right mouth corner
            ], dtype="double")
        except IndexError:
            return -200, -200, -200  # Handle cases where landmarks are not fully detected

        # Define 3D model points for the face
        model_points = np.array([
            (0.0, 0.0, 0.0),            # Nose tip
            (0.0, -63.6, -12.5),        # Chin
            (-43.3, 32.7, -26.0),       # Left eye outer corner
            (43.3, 32.7, -26.0),        # Right eye outer corner
            (-28.9, -28.9, -24.1),      # Left mouth corner
            (28.9, -28.9, -24.1)        # Right mouth corner
        ])

        # Define the camera matrix
        focal_length = w
        center = (w / 2, h / 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")

        # Assume no lens distortion
        dist_coeffs = np.zeros((4, 1))

        # Solve for head pose using solvePnP
        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return 0, 0, 0  # Head pose estimation failed

        # Refine the pose estimation using solvePnPRefineLM
        rotation_vector, translation_vector = cv2.solvePnPRefineLM(
            model_points, image_points, camera_matrix, dist_coeffs, rotation_vector, translation_vector
        )

        # Convert rotation vector to rotation matrix
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

        # Calculate Euler angles (pitch, yaw, roll) from the rotation matrix
        pitch, yaw, roll = self.rotationMatrixToEulerAngles(rotation_matrix)

        # Ensure angles are valid
        if pitch is None or yaw is None or roll is None:
            return -200, -200, -200

        return pitch, yaw, roll