
#!pip install albumentations pillow faiss-cpu tqdm transformers torch

# |%%--%%| <cCA9QsHWg2|vHNp9gEGEg>

#!pip install scikit-learn


# |%%--%%| <vHNp9gEGEg|NDP26LuFVb>

import time
import cv2
import os
import numpy as np
import faiss
import torch
import pickle
import gc
from tqdm import tqdm
from PIL import Image
from transformers import ViTModel, AutoImageProcessor
import albumentations as A
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import random

class DinoFaceRecognition:
    def __init__(self, src_dir=None):
        self.src_dir = src_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model_name = "facebook/dino-vits8"
        self.model = ViTModel.from_pretrained(self.model_name).to(self.device)
        self.model.eval()
        self.processor = AutoImageProcessor.from_pretrained(self.model_name)

        self.index = None
        self.labels = []
        self.class_to_id = {}
        self.id_to_class = {}




    def create_empty_index(self):
        dim = 384  # Kích thước vector (tuỳ thuộc vào mô hình của bạn)
        self.index = faiss.IndexFlatL2(dim)

    

    def augment_image(self, image_list, augment_ratio=0.5):
        augmented_images = []
        if not image_list:
            return []

        selected_indices = random.sample(range(len(image_list)), int(len(image_list) * augment_ratio))

        transforms = [
            A.Compose([A.Resize(256, 256), A.CoarseDropout(max_holes=1, max_height=32, max_width=32, p=1.0)]),
            A.Compose([A.Resize(256, 256), A.GaussNoise(var_limit=(10.0, 50.0), p=1.0)]),
            A.Compose([A.Resize(256, 256), A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1.0)]),
            A.Compose([A.Resize(256, 256), A.Rotate(limit=15, p=1.0)]),
            A.Compose([A.Resize(256, 256), A.HorizontalFlip(p=1.0)]),
            A.Compose([A.Resize(256, 256), A.ToGray(p=1.0)]),
        ]

        for idx in selected_indices:
            image = image_list[idx]
            if isinstance(image, np.ndarray):
                if len(image.shape) == 2:
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                elif image.shape[2] == 1:
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                elif image.shape[2] == 3:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    continue

            for aug in transforms:
                try:
                    augmented = aug(image=image)
                    aug_img = augmented['image']
                    if aug_img is not None and aug_img.shape[-1] == 3:
                        augmented_images.append(aug_img.astype(np.uint8))
                except:
                    continue

        # Trả về toàn bộ ảnh gốc + ảnh đã augment
        resized_originals = [cv2.resize(img, (256, 256)) for img in image_list]
        return resized_originals + augmented_images

    def load_data(self, faiss_index_path=None, metadata_path=None):
        if faiss_index_path and metadata_path:
            self.index = faiss.read_index(faiss_index_path)
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
                self.labels = metadata['labels']
                self.class_to_id = metadata['label_to_id']
                self.id_to_class = {v: k for k, v in self.class_to_id.items()}

    def extract_features(self, images, normalize=False):
        try:
            if not isinstance(images, list):
                images = [images]
            valid_images = []
            for img in images:
                if img is None:
                    continue
                if isinstance(img, np.ndarray):
                    if len(img.shape) == 3 and img.shape[2] == 3:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    else:
                        continue
                elif not isinstance(img, Image.Image):
                    continue
                valid_images.append(img)

            if not valid_images:
                return None

            inputs = self.processor(images=valid_images, return_tensors="pt", padding=True).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            if normalize:
                embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
            return embeddings
        except:
            return None

    def save_index(self, save_path):
        if self.index is not None and save_path:
            faiss.write_index(self.index, save_path + '.faiss')
            with open(f"{save_path}_metadata.pkl", "wb") as f:
                pickle.dump({
                    "labels": self.labels,
                    "label_to_id": self.class_to_id
                }, f)

    def train_in_batches(self, faiss_index_path=None, batch_size=10):
        if not self.src_dir:
            raise ValueError("Source directory (src_dir) not specified")

        self.labels = []
        all_class_names = sorted([name for name in os.listdir(self.src_dir) if not name.startswith('.')])
        total_labels = len(all_class_names)

        for i in tqdm(range(0, total_labels, batch_size)):
            batch_class_names = all_class_names[i:i + batch_size]
            print(f"[Batch {i // batch_size + 1}] Training on classes: {batch_class_names} ({i + len(batch_class_names)} / {total_labels})")

            images = []
            labels = []

            for class_name in batch_class_names:
                class_dir = os.path.join(self.src_dir, class_name)
                if os.path.isdir(class_dir):
                    for img_name in os.listdir(class_dir):
                        img_path = os.path.join(class_dir, img_name)
                        if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                            img = cv2.imread(img_path)
                            if img is None:
                                continue
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            images.append(img)
                            labels.append(class_name)

            augmented_imgs = self.augment_image(images, augment_ratio=0.4)
            images.extend(augmented_imgs)
            labels.extend([labels[i] for i in random.sample(range(len(labels)), len(augmented_imgs))])

            if not images:
                continue

            for label in set(labels):
                if label not in self.class_to_id:
                    new_id = len(self.class_to_id)
                    self.class_to_id[label] = new_id
                    self.id_to_class[new_id] = label

            features = self.extract_features(images, normalize=False)
            if features is None:
                continue

            label_to_features = {}
            for feat, label in zip(features, labels):
                if label not in label_to_features:
                    label_to_features[label] = []
                label_to_features[label].append(feat)

            all_features = []
            all_labels = []
            centroids = []
            centroid_labels = []
            for label, feats in label_to_features.items():
                feats_np = np.vstack(feats)
                all_features.append(feats_np)
                all_labels.extend([self.class_to_id[label]] * len(feats_np))
                centroid = np.mean(feats_np, axis=0, keepdims=True)
                centroids.append(centroid)
                centroid_labels.append(self.class_to_id[label])

            all_features = np.vstack(all_features)
            centroids = np.vstack(centroids)

            if self.index is None:
                dim = centroids.shape[1]
                self.index = faiss.IndexFlatL2(dim)
            self.index.add(all_features.astype('float32'))
            self.index.add(centroids.astype('float32'))
            self.labels.extend(all_labels)
            self.labels.extend(centroid_labels)

            print(f"[INFO] Batch Stats → Original: {len(labels) - len(augmented_imgs)}, Augmented: {len(augmented_imgs)}, Total: {len(labels)}, Feature Vectors: {len(all_labels)}, Centroids: {len(centroids)}")
            self.save_index(faiss_index_path)

            gc.collect()
            torch.cuda.empty_cache()
  

    def recognize_face_topk(self, query_img, threshold=3200, top_k=5):
        """
        Nhận diện khuôn mặt bằng FAISS, trả về label có khoảng cách nhỏ nhất
        :param query_img: ảnh đầu vào (numpy array, BGR)
        :param threshold: ngưỡng L2 distance, nếu lớn hơn thì xem là Unknown
        :param top_k: số lượng kết quả gần nhất
        :return: [(label, distance)]
        """
        if query_img is None or query_img.size == 0:
            return [("Invalid Image", 0.0)]

        try:
            # Chuyển ảnh sang RGB và trích xuất embedding
            rgb_img = cv2.cvtColor(query_img, cv2.COLOR_BGR2RGB)
            query_embed = self.extract_features([rgb_img], normalize=False)

            if query_embed is None:
                return [("No Features Extracted", 0.0)]

            # Tìm top_k vector gần nhất
            similarities, indices = self.index.search(query_embed.astype('float32'), k=top_k)

            votes = {}
            for i in range(top_k):
                idx = indices[0][i]
                dist = float(similarities[0][i])

                # Nếu không tìm thấy vector nào
                if idx == -1 or idx >= len(self.labels):
                    continue

                label_id = self.labels[idx]
                label = self.id_to_class.get(label_id, "Unknown")

                if label not in votes:
                    votes[label] = []
                votes[label].append(dist)

            # Nếu không có label nào hợp lệ
            if not votes:
                return [("Unknown", float('inf'))]

            # Lấy label có khoảng cách nhỏ nhất
            label_scores = {label: np.min(dists) for label, dists in votes.items()}

            print("[Top-k distances]")
            for label, dists in votes.items():
                print(f"Label: {label} | Distances: {['{:.2f}'.format(d) for d in dists]}")

            best_label = min(label_scores, key=label_scores.get)
            best_score = label_scores[best_label]

            # So sánh với threshold
            if best_score <= threshold:
                return [(best_label, best_score)]
            else:
                return [("Unknown", best_score)]

        except Exception as e:
            print(f"[ERROR] in recognize_face_topk: {e}")
            return [("Error", 0.0)]
  
  
      
    def print_faiss_size(self, faiss_file_path):
          if os.path.exists(faiss_file_path):
              size_in_bytes = os.path.getsize(faiss_file_path)
              size_in_mb = size_in_bytes / (1024 * 1024)
              print(f"[INFO] FAISS Index size: {size_in_mb:.2f} MB ({size_in_bytes} bytes)")
          else:
              print(f"[WARN] FAISS file not found: {faiss_file_path}")
  
      
    def evaluate_on_testset(self, test_dir, threshold=0.5, top_k=5):
          true_labels = []
          predicted_labels = []
          scores = []
  
          class_names = sorted(os.listdir(test_dir))
          for label in class_names:
              class_path = os.path.join(test_dir, label)
              if not os.path.isdir(class_path):
                  continue
              for img_name in os.listdir(class_path):
                  if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                      img_path = os.path.join(class_path, img_name)
                      img = cv2.imread(img_path)
                      if img is None:
                          continue
                      result = self.recognize_face_topk(img, threshold=threshold, top_k=top_k)[0]
                      pred_label, score = result
                      true_labels.append(label)
                      print(f'pred_label: {pred_label} | true_label: {label} | score: {score}')
                      predicted_labels.append(pred_label)
                      scores.append(score)
  
          acc = accuracy_score(true_labels, predicted_labels)
          f1 = f1_score(true_labels, predicted_labels, average='macro')
  
          label_list = sorted(set(true_labels + predicted_labels))
          label_to_idx = {label: idx for idx, label in enumerate(label_list)}
          y_true = [label_to_idx[l] for l in true_labels]
          y_score_matrix = np.zeros((len(scores), len(label_list)))
          for i, (pl, sc) in enumerate(zip(predicted_labels, scores)):
              if pl in label_to_idx:
                  y_score_matrix[i][label_to_idx[pl]] = sc
  
          try:
              roc_auc = roc_auc_score(y_true, y_score_matrix, multi_class='ovr')
          except:
              roc_auc = "Cannot compute ROC AUC (possibly not enough classes)"
  
          return {
              "Accuracy": acc,
              "F1 Score (macro)": f1,
              "ROC AUC": roc_auc
          }


# |%%--%%| <NDP26LuFVb|ZhNQRl0r0E>

#dino = DinoFaceRecognition(src_dir='train_img/')
# 🆕 Train with augmentation
#dino.train_in_batches(faiss_index_path = 'faiss_index', batch_size=1)

# |%%--%%| <ZhNQRl0r0E|12iJQrnmCX>

#dino.load_data('faiss_index.faiss', 'faiss_index_metadata.pkl')

# |%%--%%| <12iJQrnmCX|fgwVycVFoV>

#dino.print_faiss_size('faiss_index.faiss')
#|%%--%%| <fgwVycVFoV|mJYsVXolyl>
#if dino.index is not None:
#    print(f"[INFO] FAISS Index contains {dino.index.ntotal} vectors.")
#else:
#    print("[WARN] FAISS index not initialized.")
#
# |%%--%%| <mJYsVXolyl|yhNBLcwRVB>

#tester = DinoFaceRecognition()
#tester.load_data(faiss_index_path="faiss_index.faiss", metadata_path="faiss_index_metadata.pkl")

#results = tester.evaluate_on_testset(test_dir="test", threshold=4500, top_k=5)
#
#print("Accuracy:", results["Accuracy"])
#print("F1 Score:", results["F1 Score (macro)"])
#print("ROC AUC:", results["ROC AUC"])


# |%%--%%| <yhNBLcwRVB|LTgFhL9ZQQ>



# |%%--%%| <LTgFhL9ZQQ|yfDCvykxO3>


