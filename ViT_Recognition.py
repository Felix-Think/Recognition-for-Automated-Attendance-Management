import os
import numpy as np
import cv2
import torch
import faiss
from transformers import ViTImageProcessor, ViTModel
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import pickle
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
        
    def load_data(self, train = True, faiss_index_path = None, metadata_path = None):
        """Load images and labels from directory structure: src_dir/class_name/image.jpg"""
        if train:
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
        else:
            # Load faiss index and metadata
            self.index = faiss.read_index(faiss_index_path)
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
                self.labels = metadata['labels']
                self.class_to_id = metadata['label_to_id']
            return None, None

    def extract_features(self, images):
        """Extract ViT embeddings (CLS token)"""
        inputs = self.processor(images=images, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state[:, 0, :].cpu().numpy()  # CLS token

    def build_and_save_faiss_index(self, features, save_path=None): # save_path = faiss index path
        """Create FAISS index for fast similarity search"""
        dim = features.shape[1]
        self.index = faiss.IndexFlatL2(dim)  # L2 distance
        self.index.add(features.astype('float32'))

        #Save index and metadata
        faiss.write_index(self.index, save_path + '.faiss') # Save index

        with open(f"{save_path}_metadata.pkl", "wb") as f:
            pickle.dump({"labels": self.labels, "label_to_id": self.class_to_id}, f) # Save metadata, metadata include labels and mapping from label to id , or we can call it class_to_id 

    def add_new_user(self, img_paths, user_name, faiss_index_path, metadata_path):
        """Add new user embedding to Faiss index"""
        if self.index is None: 
            self.index, self.labels, self.class_to_id = self.load_data(train = False, faiss_index_path = faiss_index_path, metadata_path = metadata_path)

        if user_name not in self.class_to_id:
            self.class_to_id[user_name] = len(self.class_to_id)

        for img_path in img_paths:
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            embedding = self.extract_features([img])
            self.index.add(embedding.astype('float32'))
        self.labels.append(self.class_to_id[user_name])
        print(f"Added user: {user_name}")
        # Save updated Index and metadata
        faiss.write_index(self.index, faiss_index_path + '.faiss')
        with open(metadata_path, "wb") as f:
            pickle.dump({"labels": self.labels, "label_to_id": self.class_to_id}, f)


    def recognize_face_1(self, query_img_path, threshold=0.9):
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
    # recognize_face for list of images

    def recognize_face_2(self, query_img_list, threshold=0.9):
        """Recognize face using FAISS search"""
        #
        results = []
        for image in query_img_list:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            query_embed = self.extract_features([image])

            D, I = self.index.search(query_embed.astype('float32'), k=1)
            distance = D[0][0]
            pred_id = self.labels[I[0][0]]
            # Convert distance to cosine similarity (assuming embeddings are normalized)
            similarity = 1 - distance / 2  
            if similarity > threshold:
                user_name = [k for k, v in self.class_to_id.items() if v == pred_id][0]
                results.append((user_name, pred_id, similarity))
            else:
                results.append(("Unknown", pred_id, similarity))

        return results
            
# Usage Example
if __name__ == "__main__":
    vit = ViTFaceRecognition(src_dir= os.path.join('train_img'))
    images, labels = vit.load_data(train=False, faiss_index_path='faiss_index.faiss', metadata_path='faiss_index_metadata.pkl')
    #features = vit.extract_features(images)
    #vit.build_and_save_faiss_index(features, save_path='faiss_index') #if file is not exist, you have to train index for images
    # Test recognition
    result, score = vit.recognize_face_1('train_img/Long/cropped_face_10.jpg')
    print(f"Recognized: {result} (Score: {score:.2f})")

    # Test new User
#    usr_dir = 'train_img/Michael_Powell'
#    paths_new_user = os.listdir(usr_dir)
#    usr_paths = [os.path.join(usr_dir, path) for path in paths_new_user]
#    vit.add_new_user(usr_paths, 'Michael_Powell', faiss_index_path='faiss_index.faiss', metadata_path='faiss_index_metadata.pkl')
    # Test recognition after adding new user

#|%%--%%| <QmmjrfLpJ4|0N46Aqd1NS>
    
    image = cv2.imread('train_img/Michael_Powell/Michael_Powell_0002.jpg')
    image = [image]    
    result = vit.recognize_face_2(image)
    print(result)
    
