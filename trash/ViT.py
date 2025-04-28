import os
import numpy as np
import cv2
import torch
import faiss
from transformers import ViTImageProcessor, ViTModel
from sklearn.model_selection import train_test_split
from tqdm import tqdm

class ViTFaceRecognition:
    def __init__(self, src_dir='data/train_img/'):
        self.src_dir = src_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load pretrained ViT (không dùng classification head)
        self.processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
        self.model = ViTModel.from_pretrained('google/vit-base-patch16-224').to(self.device)
        self.model.eval()
        
        # Faiss index
        self.index = None
        self.labels = []
        self.class_to_id = {}
        
    def load_data(self):
        """Load images and labels from directory structure: src_dir/class_name/image.jpg"""
        self.class_to_id = {cls: idx for idx, cls in enumerate(os.listdir(self.src_dir))}
        self.labels = []
        images = []
        
        for cls in os.listdir(self.src_dir):
            cls_dir = os.path.join(self.src_dir, cls)
            for img_name in tqdm(os.listdir(cls_dir), desc=f"Loading {cls}"):
                img_path = os.path.join(cls_dir, img_name)
                img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
                images.append(img)
                self.labels.append(self.class_to_id[cls])
        
        return images, np.array(self.labels)

    def extract_features(self, images):
        """Extract ViT embeddings (CLS token)"""
        inputs = self.processor(images=images, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state[:, 0, :].cpu().numpy()  # CLS token

    def build_faiss_index(self, features):
        """Create FAISS index for fast similarity search"""
        dim = features.shape[1]
        self.index = faiss.IndexFlatL2(dim)  # L2 distance
        self.index.add(features.astype('float32'))

    def add_new_user(self, img_path, user_name):
        """Add new user embedding to Faiss index"""
        if user_name not in self.class_to_id:
            self.class_to_id[user_name] = len(self.class_to_id)
        
        img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
        embedding = self.extract_features([img])
        self.index.add(embedding.astype('float32'))
        self.labels.append(self.class_to_id[user_name])
        print(f"Added user: {user_name}")

    def recognize_face(self, query_img_path, threshold=0.9):
        """Recognize face using FAISS search"""
        img = cv2.cvtColor(cv2.imread(query_img_path), cv2.COLOR_BGR2RGB)
        query_embed = self.extract_features([img])
        
        D, I = self.index.search(query_embed.astype('float32'), k=1)
        distance = D[0][0]
        pred_id = self.labels[I[0][0]]
        
        # Convert distance to cosine similarity (assuming embeddings are normalized)
        similarity = 1 - distance / 2  
        if similarity > threshold:
            user_name = [k for k, v in self.class_to_id.items() if v == pred_id][0]
            return user_name, similarity
        else:
            return "Unknown", similarity

# Usage Example
if __name__ == "__main__":
    vit = ViTFaceRecognition(src_dir="data/train_img/")
    images, labels = vit.load_data()
    features = vit.extract_features(images)
    vit.build_faiss_index(features)
    
    # Test recognition
    result, score = vit.recognize_face("data/query.jpg")
    print(f"Recognized: {result} (Score: {score:.2f})")
