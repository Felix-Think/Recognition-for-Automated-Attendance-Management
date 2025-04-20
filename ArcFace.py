import insightface
from insightface.app import FaceAnalysis
import faiss
import numpy as np
import cv2
import os
from tqdm import tqdm

class ArcFaceRecognition:
    def __init__(self, src_dir='Datasets/train_img/'):
        self.src_dir = src_dir

        self.app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])  # Thay CUDA bằng CPU
        self.app.prepare(ctx_id=-1)  # ctx_id=-1 cho CPU
        #self.app = FaceAnalysis(name="buffalo_l", providers=["CUDAExecutionProvider"])
        #self.app.prepare(ctx_id=0)  # GPU: ctx_id=0, CPU: ctx_id=-1
        
        # Faiss index
        self.index = None
        self.labels = []
        self.class_to_id = {}
    
    def load_data(self):
        """Load images and extract embeddings using InsightFace"""
        self.class_to_id = {cls: idx for idx, cls in enumerate(os.listdir(self.src_dir))}
        self.labels = []
        embeddings = []
        
        for cls in os.listdir(self.src_dir):
            cls_dir = os.path.join(self.src_dir, cls)
            for img_name in tqdm(os.listdir(cls_dir), desc=f"Processing {cls}"):
                img_path = os.path.join(cls_dir, img_name)
                img = cv2.imread(img_path)
                faces = self.app.get(img)
                if len(faces) > 0:
                    embedding = faces[0].embedding
                    embeddings.append(embedding)
                    self.labels.append(self.class_to_id[cls])
        
        return np.array(embeddings), np.array(self.labels)

    def build_faiss_index(self, embeddings):
        """Create FAISS index"""
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings.astype('float32'))

    def add_new_user(self, img_path, user_name):
        """Add new user to Faiss index"""
        if user_name not in self.class_to_id:
            self.class_to_id[user_name] = len(self.class_to_id)
        
        img = cv2.imread(img_path)
        faces = self.app.get(img)
        if len(faces) > 0:
            embedding = faces[0].embedding
            self.index.add(np.array([embedding], dtype='float32'))
            self.labels.append(self.class_to_id[user_name])
            print(f"Added user: {user_name}")

    def recognize_face(self, query_img_path, threshold=1.0):
        """Recognize face using FAISS"""
        img = cv2.imread(query_img_path)
        faces = self.app.get(img)
        if len(faces) > 0:
            query_embed = faces[0].embedding
            D, I = self.index.search(np.array([query_embed], dtype='float32'), k=1)
            distance = D[0][0]
            pred_id = self.labels[I[0][0]]
            
            if distance < threshold:
                user_name = [k for k, v in self.class_to_id.items() if v == pred_id][0]
                return user_name, distance
        return "Unknown", float('inf')

# Usage Example
if __name__ == "__main__":
    arcface = ArcFaceRecognition(src_dir= 'Datasets/train_img/')
    embeddings, labels = arcface.load_data()
    arcface.build_faiss_index(embeddings)
    
    # Test recognition
    result, distance = arcface.recognize_face("Datasets/train_img/Long/cropped_face_10.jpg")
    print(f"Recognized: {result} (Distance: {distance:.2f})")
