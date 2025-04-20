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
        
        # Load pretrained ViT
        self.processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
        self.model = ViTModel.from_pretrained('google/vit-base-patch16-224').to(self.device)
        self.model.eval()
        
        # Faiss index
        self.index = None
        self.labels = []
        self.class_to_id = {}
        self.id_to_class = {}  # Reverse mapping for faster lookup
    
    def load_data(self, faiss_index_path=None, metadata_path=None):
        """Load images and labels from directory structure: src_dir/class_name/image.jpg"""
        if faiss_index_path and metadata_path:
            self.index = faiss.read_index(faiss_index_path)
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
                self.labels = metadata['labels']
                self.class_to_id = metadata['label_to_id']
                self.id_to_class = {v: k for k, v in self.class_to_id.items()}
    
    def extract_features(self, images, normalize=True):
        """Extract ViT embeddings (CLS token) with optional normalization"""
        inputs = self.processor(images=images, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        if normalize:
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings

    def build_and_save_faiss_index(self, features, save_path=None):
        """Create FAISS index for fast similarity search"""
        dim = features.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # Using Inner Product for cosine similarity
        self.index.add(features.astype('float32'))

        # Save index and metadata
        if save_path:
            faiss.write_index(self.index, save_path + '.faiss')
            with open(f"{save_path}_metadata.pkl", "wb") as f:
                pickle.dump({
                    "labels": self.labels,
                    "label_to_id": self.class_to_id
                }, f)
    
    def train(self, faiss_index_path=None):
        """Train the model and save the FAISS index"""
        images = []
        labels = []
        
        # Load images and labels
        for class_name in tqdm(os.listdir(self.src_dir), desc="Loading images"):
            class_dir = os.path.join(self.src_dir, class_name)
            if os.path.isdir(class_dir):
                for img_name in os.listdir(class_dir):
                    img_path = os.path.join(class_dir, img_name)
                    if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                        try:
                            img = cv2.imread(img_path)
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            images.append(img)
                            labels.append(class_name)
                        except Exception as e:
                            print(f"Error loading {img_path}: {e}")

        # Create label mappings
        unique_labels = sorted(set(labels))
        self.class_to_id = {label: i for i, label in enumerate(unique_labels)}
        self.id_to_class = {i: label for label, i in self.class_to_id.items()}
        
        # Convert labels to IDs
        label_ids = [self.class_to_id[label] for label in labels]
        self.labels = label_ids

        # Extract features
        features = self.extract_features(images)

        # Build and save FAISS index
        self.build_and_save_faiss_index(features, save_path=faiss_index_path)

    def add_new_user(self, img_paths, user_name, faiss_index_path, metadata_path):
        """Add new user embedding to Faiss index"""
        # Load existing index and metadata
        self.load_data(faiss_index_path, metadata_path)
        
        # Assign ID for new user
        if user_name not in self.class_to_id:
            new_id = len(self.class_to_id)
            self.class_to_id[user_name] = new_id
            self.id_to_class[new_id] = user_name
        
        user_id = self.class_to_id[user_name]
        
        # Process new images
        new_embeddings = []
        for img_path in img_paths:
            try:
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                embedding = self.extract_features([img])
                new_embeddings.append(embedding)
                self.labels.append(user_id)
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        if new_embeddings:
            new_embeddings = np.vstack(new_embeddings)
            self.index.add(new_embeddings.astype('float32'))
            
            # Save updated index and metadata
            faiss.write_index(self.index, faiss_index_path)
            with open(metadata_path, "wb") as f:
                pickle.dump({
                    "labels": self.labels,
                    "label_to_id": self.class_to_id
                }, f)
            
            print(f"Added {len(new_embeddings)} embeddings for user: {user_name}")
        else:
            print("No valid images found for the new user")

    def recognize_face(self, query_img, threshold=0.9, top_k=1):
        """
        Recognize face using FAISS search
        
        Args:
            query_img: numpy.ndarray - Input face image (BGR format)
            threshold: float - Similarity threshold for recognition
            top_k: int - Number of top matches to return
            
        Returns:
            List of tuples (user_name, similarity) for top_k matches
        """
        if query_img is None or query_img.size == 0:
            return [("Invalid Image", 0.0)]
        
        try:
            # Convert to RGB and extract features
            query_img = cv2.cvtColor(query_img, cv2.COLOR_BGR2RGB)
            query_embed = self.extract_features([query_img])
            
            # Search in FAISS index (using inner product for cosine similarity)
            similarities, indices = self.index.search(query_embed.astype('float32'), k=top_k)
            
            results = []
            for i in range(top_k):
                pred_id = self.labels[indices[0][i]]
                similarity = float(similarities[0][i])  # Convert numpy float to Python float
                user_name = self.id_to_class.get(pred_id, "Unknown")
                
                if similarity > threshold:
                    results.append((user_name, similarity))
                else:
                    results.append(("Unknown", similarity))
            
            return results
        except Exception as e:
            print(f"Error in face recognition: {e}")
            return [("Error", 0.0)]

#|%%--%%| <jVldExvb46|0GHGEMZjBH>

# Usage Example
#vit = ViTFaceRecognition(src_dir= 'train_img/')

    # Train the model and save the FAISS index
#vit.train(faiss_index_path='faiss_index')

#|%%--%%| <0GHGEMZjBH|0Z708JLZE3>
    # Load the index and metadata
#vit.load_data(faiss_index_path='faiss_index.faiss', metadata_path='faiss_index_metadata.pkl')
#print(vit.index.ntotal) # Print number of images in index
#|%%--%%| <0Z708JLZE3|Ex0W471JSf>

    # Test recognition
#result = vit.recognize_face(cv2.imread('train_img/Long/cropped_face_2.jpg'), top_k=3)
#print(f"Recognized: {result[0][0]} (Score: {result[0][1]:.2f})")

    
#|%%--%%| <Ex0W471JSf|zMQsYA7mP2>


#img_path = 'Datasets/D0010'
#add_new_user = os.listdir(img_path)
#add_new_user = [os.path.join(img_path, path) for path in add_new_user] # Lay duong dan de cac anh cua ID

#vit.add_new_user(add_new_user, 'D0010', faiss_index_path='faiss_index.faiss', metadata_path='faiss_index_metadata.pkl')
#|%%--%%| <zMQsYA7mP2|b4iawZogYP>
# Test recognition after adding new user
#result = vit.recognize_face(cv2.imread('Datasets/D001/face_1.png'), top_k=3)
#print(f"Recognized: {result[0][0]} (Score: {result[0][1]:.2f})")
