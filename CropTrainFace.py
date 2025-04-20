import os
import cv2
import FaceDetection as FD
# Path to the train directory
train_dir = 'vggface2/versions/1/train'
FaceDetect = FD.FaceDetection()
new_dir = 'vggface2/versions/1/train/cropped'
# Iterate through each folder in the train directory
for folder_name in os.listdir(train_dir):
    folder_path = os.path.join(train_dir, folder_name)
    if os.path.isdir(folder_path):
        # Iterate through each image in the folder
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            if os.path.isfile(image_path):
                # Read the image using cv2
                frame = cv2.imread(image_path)
                if frame is not None:
                    face_crops = FaceDetect.detectFace(frame)
                    # Save the cropped faces
                    for i, face_crop in enumerate(face_crops):
                        # Save the cropped face image
                        save_path = os.path.join(folder_path, f"cropped_{i}_{image_name}")
                        cv2.imwrite(save_path, face_crop)
                

