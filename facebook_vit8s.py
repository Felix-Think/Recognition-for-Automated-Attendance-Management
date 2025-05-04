import time
import cv2
import os
import numpy as np
import faiss
import torch
import pickle
from tqdm import tqdm
from PIL import Image
from transformers import ViTModel, AutoImageProcessor

class DinoFaceRecognition:
    def __init__(self, src_dir=None):
        """Initialize DinoFaceRecognition with DINO-ViTS8 model"""
        self.src_dir = src_dir
        self.device = torch.device("cpu")
        
        # Load DINO-ViTS8 model and processor
        self.model_name = "facebook/dino-vits8"
        self.model = ViTModel.from_pretrained(self.model_name).to(self.device)
        self.model.eval()
        self.processor = AutoImageProcessor.from_pretrained(self.model_name)
        
        # FAISS index and metadata
        self.index = None
        self.labels = []
        self.class_to_id = {}
        self.id_to_class = {}

    def load_data(self, faiss_index_path=None, metadata_path=None):
        """Load FAISS index and metadata from saved files"""
        if faiss_index_path and metadata_path:
            try:
                self.index = faiss.read_index(faiss_index_path)
                with open(metadata_path, 'rb') as f:
                    metadata = pickle.load(f)
                    self.labels = metadata['labels']
                    self.class_to_id = metadata['label_to_id']
                    self.id_to_class = {v: k for k, v in self.class_to_id.items()}
            except Exception as e:
                print(f"Error loading index/metadata: {e}")
                raise

    def extract_features(self, images, normalize=True):
        """Extract ViT embeddings (CLS token) with optional normalization"""
        try:
            if not isinstance(images, list):
                images = [images]
            
            # Preprocess images
            inputs = self.processor(images=images, return_tensors="pt", padding=True).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()  # CLS token, shape: [batch, 384]
            
            if normalize:
                embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
            return embeddings
        except Exception as e:
            print(f"Error in feature extraction: {e}")
            return None

    def build_and_save_faiss_index(self, features, save_path=None):
        """Create FAISS index for fast similarity search"""
        try:
            if features is None or features.size == 0:
                raise ValueError("No features provided for FAISS index")
                
            dim = features.shape[1]
            self.index = faiss.IndexFlatIP(dim)  # Inner Product for cosine similarity
            self.index.add(features.astype('float32'))

            # Save index and metadata
            if save_path:
                faiss.write_index(self.index, save_path + '.faiss')
                with open(f"{save_path}_metadata.pkl", "wb") as f:
                    pickle.dump({
                        "labels": self.labels,
                        "label_to_id": self.class_to_id
                    }, f)
        except Exception as e:
            print(f"Error building/saving FAISS index: {e}")
            raise

    def train(self, faiss_index_path=None):
        """Train the model and save the FAISS index"""
        if not self.src_dir:
            raise ValueError("Source directory (src_dir) not specified")
            
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
                            if img is None:
                                print(f"Failed to load image: {img_path}")
                                continue
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            images.append(img)
                            labels.append(class_name)
                        except Exception as e:
                            print(f"Error loading {img_path}: {e}")

        if not images:
            raise ValueError("No valid images found in the dataset")

        # Create label mappings
        unique_labels = sorted(set(labels))
        self.class_to_id = {label: i for i, label in enumerate(unique_labels)}
        self.id_to_class = {i: label for label, i in self.class_to_id.items()}
        
        # Convert labels to IDs
        self.labels = [self.class_to_id[label] for label in labels]

        # Extract features
        features = self.extract_features(images)
        if features is None:
            raise ValueError("Feature extraction failed")

        # Build and save FAISS index
        self.build_and_save_faiss_index(features, save_path=faiss_index_path)

    def add_new_user(self, img_paths, user_name, faiss_index_path, metadata_path):
        """Add new user embedding to FAISS index"""
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
                if img is None:
                    print(f"Failed to load image: {img_path}")
                    continue
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                embedding = self.extract_features([img])
                if embedding is not None:
                    new_embeddings.append(embedding)
                    self.labels.append(user_id)
                else:
                    print(f"No features extracted for: {img_path}")
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
            return True
        else:
            print("No valid images found for the new user")
            return False

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
            if query_embed is None:
                return [("No Features Extracted", 0.0)]
            
            # Search in FAISS index
            similarities, indices = self.index.search(query_embed.astype('float32'), k=top_k)
            
            results = []
            for i in range(top_k):
                pred_id = self.labels[indices[0][i]]
                similarity = float(similarities[0][i])
                user_name = self.id_to_class.get(pred_id, "Unknown")
                
                if similarity > threshold:
                    results.append((user_name, similarity))
                else:
                    results.append(("Unknown", similarity))
            
            return results
        except Exception as e:
            print(f"Error in face recognition: {e}")
            return [("Error", 0.0)]
#|%%--%%| <2vJrQTmxXb|lwZreMXTXz>

# Example usage
if __name__ == "__main__":
    dino = DinoFaceRecognition(src_dir='train_img/')
    dino.train(faiss_index_path='faiss_index')
#|%%--%%| <lwZreMXTXz|BnCjgv4ISY>
    
    # Add new user
    label = 'D0007'
    valid_exts = ('.png', '.jpg', '.jpeg')
    src_dir = os.path.join('Datasets', label)
    usr_paths = [
        os.path.join(src_dir, f) for f in os.listdir(src_dir) 
        if f.lower().endswith(valid_exts)
    ]
    dino.add_new_user(
        usr_paths, 
        label,
        faiss_index_path='faiss_index.faiss',
        metadata_path='faiss_index_metadata.pkl'
    )
#|%%--%%| <BnCjgv4ISY|6X4Q4Z3H4D>
    
    # Test recognition
    test_img = cv2.imread("train_img/Long/cropped_face_1.jpg")
    if test_img is not None:
        start = time.time()
        result = dino.recognize_face(test_img)
        print(f"Recognition result: {result}")
        print(f"Inference time: {time.time() - start} seconds")
    else:
        print("Failed to load test image")
