import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from transformers import ViTImageProcessor, ViTForImageClassification
from sklearn.model_selection import train_test_split
import faiss

# Class Adapter
class Adapter(nn.Module):
    def __init__(self, input_dim=768, output_dim=768):
        super(Adapter, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.fc(x)
        return self.activation(x)

# Class VitAdapter với Faiss
class VitAdapter:
    def __init__(self, src_dir='../../train_folder/train_img/', adapter_path=None, use_hnsw=False):
        self.src_dir = src_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
        self.model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224').to(self.device)
        self.model.eval()
        # Tắt gradient cho ViT để không train lại
        for param in self.model.parameters():
            param.requires_grad = False
        
        self.adapter = Adapter().to(self.device)
        if adapter_path and os.path.exists(adapter_path):
            self.adapter.load_state_dict(torch.load(adapter_path))
            print(f"Loaded adapter from {adapter_path}")
        self.adapter.eval()
        
        self.classes = {img_class: idx for idx, img_class in enumerate(os.listdir(src_dir))}
        self.data = {'images': [], 'labels': []}
        
        self.embedding_dim = 768
        if use_hnsw:
            self.index = faiss.IndexHNSWFlat(self.embedding_dim, 32)
        else:
            self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index_labels = []

    def load_data(self):
        paths_images = []
        for img_class in os.listdir(self.src_dir):
            class_dir = os.path.join(self.src_dir, img_class)
            for img in os.listdir(class_dir):
                path_image = os.path.join(class_dir, img)
                paths_images.append(path_image)
       
        for path_image in paths_images:
            img = cv2.imread(path_image)
            if img is None:
                print(f"Warning: Could not load image {path_image}")
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.data['images'].append(img)
            class_name = os.path.basename(os.path.dirname(path_image))
            self.data['labels'].append(self.classes[class_name])
        print(f"Loaded {len(self.data['images'])} images and {len(self.data['labels'])} labels.")

    def train_test_split(self):
        self.train_images, self.test_images, self.train_labels, self.test_labels = train_test_split(
            self.data['images'], self.data['labels'], test_size=0.2, random_state=42
        )

    def preprocessing(self, images, use_adapter=False):
        if isinstance(images, list):
            inputs = self.processor(images, return_tensors='pt').to(self.device)
        else:
            inputs = self.processor(images, return_tensors='pt').to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True).hidden_states[-1][:, 0, :]
        if use_adapter:
            outputs = self.adapter(outputs)  # Gradient sẽ được giữ nếu adapter.train()
        return outputs.detach().cpu().numpy()

    def ranking(self, preprocessed_query_image, top_k=10):
        query_emb = preprocessed_query_image.astype('float32')
        if len(query_emb.shape) == 1:
            query_emb = query_emb.reshape(1, -1)
        distances, indices = self.index.search(query_emb, top_k)
        scores = 1 - distances / 2
        ranked_list = indices[0]
        return ranked_list, scores[0]

    def train(self, is_split=False, is_train=False, is_save=True):
        train_images = self.data['images']
        train_labels = self.data['labels']
        if is_split:
            self.train_test_split()
            train_images = self.train_images
            train_labels = self.train_labels
        else:
            self.train_images = self.data['images']
            self.train_labels = self.data['labels']
        
        if is_train:
            print("Preprocessing data...")
            preprocessed_train_images = self.preprocessing(train_images, use_adapter=False)
            self.index.add(preprocessed_train_images.astype('float32'))
            self.index_labels = train_labels
        else:
            if os.path.exists('data_images_preprocessed.npy'):
                preprocessed_train_images = np.load('data_images_preprocessed.npy')
                self.index.add(preprocessed_train_images.astype('float32'))
                self.index_labels = list(np.load('train_labels.npy'))
                print(f"Loaded preprocessed data and added to Faiss index.")
            else:
                raise FileNotFoundError("Preprocessed data file not found. Run with is_train=True and is_save=True first.")
        
        if is_save:
            np.save('data_images_preprocessed.npy', preprocessed_train_images)
            np.save('train_labels.npy', np.array(train_labels))
            print("Preprocessed data saved.")
        return preprocessed_train_images

    def train_adapter_for_new_employee(self, new_images, new_label, epochs=10, save_path='adapter.pth'):
        self.adapter.train()
        optimizer = torch.optim.Adam(self.adapter.parameters(), lr=0.001)
        criterion = nn.PairwiseDistance(p=2)
        margin = 1.0

        valid_new_images = []
        for img in new_images:
            if img is None:
                print(f"Warning: Skipping invalid image in new_images")
                continue
            valid_new_images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not valid_new_images:
            raise ValueError("No valid images provided for new employee")
        
        new_inputs = self.processor(valid_new_images, return_tensors='pt').to(self.device)
        # Không dùng no_grad() để giữ gradient cho adapter
        vit_embs = self.model(**new_inputs, output_hidden_states=True).hidden_states[-1][:, 0, :]

        # Negative samples từ Faiss index
        n_old = self.index.ntotal
        if n_old > 0:
            indices = np.random.choice(n_old, size=min(10, n_old), replace=False)
            old_embs = torch.tensor(self.index.reconstruct_n(0, n_old)[indices]).to(self.device)
        else:
            old_embs = torch.zeros((10, self.embedding_dim)).to(self.device)

        # Huấn luyện adapter
        for epoch in range(epochs):
            optimizer.zero_grad()
            new_embs = self.adapter(vit_embs)  # Gradient được giữ
            
            pos_loss = 0
            for i in range(len(new_embs) - 1):
                dist = criterion(new_embs[i:i+1], new_embs[i+1:i+2]).mean()
                pos_loss += dist
            pos_loss /= max(1, len(new_embs) - 1)

            neg_loss = 0
            for new_emb, old_emb in zip(new_embs, old_embs):
                dist = criterion(new_emb.unsqueeze(0), old_emb.unsqueeze(0))
                neg_loss += torch.relu(margin - dist).mean()
            neg_loss /= len(new_embs)

            loss = pos_loss + neg_loss
            loss.backward()
            optimizer.step()
            print(f"Epoch {epoch}, Loss: {loss.item()}")

        torch.save(self.adapter.state_dict(), save_path)
        print(f"Adapter saved to {save_path}")

        with torch.no_grad():
            new_embs = self.adapter(vit_embs).cpu().numpy()
        self.index.add(new_embs.astype('float32'))
        self.index_labels.extend([new_label] * len(new_embs))
        return new_embs, [new_label] * len(valid_new_images)

    def reference(self, queries_img, use_adapter=False, top_k=10):
        query_images_preprocessed = self.preprocessing(queries_img, use_adapter=use_adapter)
        ranked_list, scores = self.ranking(query_images_preprocessed, top_k=top_k)
        return ranked_list, scores  




    def visualize(self, query_image, top_k=10):
        ranked_list, scores = self.reference(query_image, use_adapter=False, top_k=top_k)
        num_images = len(ranked_list)
        plt.figure(figsize=(15, 5))
        for idx, (img_idx, score) in enumerate(zip(ranked_list, scores)):
            plt.subplot(1, num_images, idx + 1)
            plt.imshow(self.data['images'][img_idx])
            plt.title(f'Similarity: {score:.4f}')
            plt.axis('off')
            plt.show()

if __name__ == '__main__':
    src_dir = os.path.join('..', '..', 'train_folder', 'train_img')
    vit_adapter = VitAdapter(src_dir=src_dir, use_hnsw=False)
    vit_adapter.load_data()

    if not os.path.exists('data_images_preprocessed.npy'):
        data_images_preprocessed = vit_adapter.train(is_split=False, is_train=True, is_save=True)
    else:
        data_images_preprocessed = vit_adapter.train(is_split=False, is_train=False, is_save=False)


    # Thêm nhân viên mới
    new_images_paths = [f"../../train_folder/train_img/Richard_Virenque/Richard_Virenque_000{i+1}" for i in range(8)]
    new_images = []
    for path in new_images_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"Error: Could not load image at {path}")
        else:
            new_images.append(img)
    
    if new_images:
        new_embs, new_labels = vit_adapter.train_adapter_for_new_employee(
            new_images, "Tim_Henman", epochs=10
        )
        updated_embeddings = np.concatenate([data_images_preprocessed, new_embs])
        updated_labels = list(np.load('train_labels.npy')) + new_labels
        np.save('data_images_preprocessed.npy', updated_embeddings)
        np.save('train_labels.npy', np.array(updated_labels))
    else:
        print("No valid images loaded for new employee. Skipping adapter training.")

    # Test với ảnh query
    query_image_path = os.path.join('..', '..', 'train_folder', 'train_img', 'Long', 'cropped_face_3.jpg')
    query_image = cv2.imread(query_image_path)
    if query_image is not None:
        query_image = cv2.cvtColor(query_image, cv2.COLOR_BGR2RGB)
        print('Query Image')
        plt.imshow(query_image)
        plt.show()

        ranked_list, scores = vit_adapter.reference(query_image)
        print("Ranked list:", ranked_list)
        print("Scores:", scores)
        vit_adapter.visualize(query_image)
    else:
        print(f"Error: Could not load query image at {query_image_path}")
