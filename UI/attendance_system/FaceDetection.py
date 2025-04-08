from ultralytics import YOLO
import cv2

class FaceDetection:
    def __init__(self, model_path="yolov8n-face.pt", camera_index=0):
        """
        Initialize the FaceDetection class.
        :param model_path: Path to the YOLOv8 model file.
        :param camera_index: Index of the camera to use.
        """
        self.model = YOLO(model_path)  # Load the YOLO model
        self.cap = cv2.VideoCapture(camera_index)  # Initialize the video capture
        if not self.cap.isOpened():
            raise Exception("Error: Unable to access the camera.")
        self.index = 0  # Used for saving images

    def detectFace(self, frame):
        """
        Process a single frame to detect faces and draw bounding boxes.
        :param frame: Input frame from the video stream.
        :return: Processed frame with bounding boxes.
        """
        results = self.model(frame)  # Detect objects in the frame
        faces = []  # List to store cropped faces
        for result in results:
            for box in result.boxes:
                # Extract bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Crop the face from the frame
                face_crop = frame[y1:y2, x1:x2]
                faces.append(face_crop)
        return faces

    def run(self):
        """
        Start the face detection process.
        """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Unable to read frame from the camera.")
                break

            # Process the frame
            processed_frame = self.process_frame(frame)

            # Display the processed frame
            cv2.imshow("Camera Feed", processed_frame)

            # Exit the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.release_resources()

    def release_resources(self):
        """
        Release the camera and close all OpenCV windows.
        """
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Initialize and run the face detection
    face_detection = FaceDetection(model_path="yolov8n-face.pt", camera_index=0)
    face_detection.run()
