import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import torch
from transformers import ViTImageProcessor, ViTForImageClassification
from sklearn.model_selection import train_test_split

class Vit:
    def __init__(self, src_dir='../../train_folder/train_img/'):
        # Init
        self.src_dir = src_dir
        # Load model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
        self.model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224').to(self.device)
        self.model.eval()
        # Lay cac class trong data
        self.classes = {img_class: idx for idx, img_class in enumerate(os.listdir(src_dir))}

        # chuan bi data cho train
        self.data = {'images': [], 'labels': []}

    def load_data(self):
        paths_images = []
        for img_class in os.listdir(self.src_dir):
            class_dir = os.path.join(self.src_dir, img_class)
            for img in os.listdir(class_dir):
                path_image = os.path.join(class_dir, img)
                paths_images.append(path_image)
       
        for path_image in paths_images:
            img = cv2.imread(path_image)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.data['images'].append(img)
            class_name = os.path.basename(os.path.dirname(path_image))
            self.data['labels'].append(self.classes[class_name])
        print(f"Loaded {len(self.data['images'])} images and {len(self.data['labels'])} labels.")

    def train_test_split(self):
        self.train_images, self.test_images, self.train_labels, self.test_labels = train_test_split(
            self.data['images'], self.data['labels'], test_size=0.2, random_state=42
        )

    def cosine_similarity(self, query_vector, src_vectors):
        query_vector = np.squeeze(query_vector) # shape (1, 768) -> (768,)
        dot_product = np.dot(src_vectors, query_vector) # shape (N, 768) * (768,) -> (N,)
        src_norm = np.linalg.norm(src_vectors, axis=1) # shape (N,)
        query_norm = np.linalg.norm(query_vector)
        cosine_similarity = dot_product / (src_norm * query_norm) # shape (N,)
        return cosine_similarity

    def preprocessing(self, images):
        if isinstance(images, list):
            inputs = self.processor(images, return_tensors='pt').to(self.device)
        else:
            inputs = self.processor(images, return_tensors='pt').to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True).hidden_states[-1][:, 0, :].detach().cpu().numpy()
        return outputs

    def ranking(self, preprocessed_query_image, preprocessed_src_images, top_k=10):
        scores = self.cosine_similarity(preprocessed_query_image, preprocessed_src_images)
        ranked_list = np.argsort(scores)[::-1][:top_k]
        scores = scores[ranked_list]
        return ranked_list, scores
    
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
            preprocessed_train_images = self.preprocessing(train_images)
        else:
            if os.path.exists('data_images_preprocessed.npy'):
                return np.load('data_images_preprocessed.npy')
            else:
                raise FileNotFoundError("Preprocessed data file not found. Run with is_train=True and is_save=True first.")
        
        if is_save:
            np.save('data_images_preprocessed.npy', preprocessed_train_images)
            np.save('train_labels.npy', np.array(train_labels))  # Lưu nhãn để sử dụng sau
            print("Preprocessed data saved to 'data_images_preprocessed.npy' and labels to 'train_labels.npy'")
        else:
            print("Preprocessed data not saved.")
        return preprocessed_train_images

    def reference(self, queries_img, data_images_preprocessed):
        query_images_preprocessed = self.preprocessing(queries_img)
        ranked_list, scores = self.ranking(query_images_preprocessed, data_images_preprocessed)
        return ranked_list, scores  

    def visualize(self, query_image, data_images_preprocessed):
        ranked_list, scores = self.ranking(preprocessed_query_image, data_images_preprocessed)
        num_images = len(ranked_list)
        plt.figure(figsize=(15, 5))
        for idx, (img_idx, score) in enumerate(zip(ranked_list, scores)):
            plt.subplot(1, num_images, idx + 1)
            plt.imshow(self.data['images'][img_idx])
            plt.title(f'Similarity: {score:.10f}')
            plt.axis('off')
            plt.show()

if __name__ == '__main__':
    src_dir = os.path.join('..', '..', 'train_folder', 'train_img')
    #src_dir = '../../train_folder/train_img/'
    classes = {img_class: idx for idx, img_class in enumerate(os.listdir(src_dir))}
    vit = Vit(src_dir=src_dir)
    vit.load_data()
    # Neu chua co data preprocessed thi train = True and Save = True, neu muon chia du lieu thi split = True
    data_images_preprocessed = vit.train(is_split = False, is_train = False, is_save = False)
    query_image = cv2.imread(os.path.join('..', '..', 'train_folder', 'train_img', 'Long', 'cropped_face_1.jpg'))
    #query_image = cv2.imread('../../train_folder/train_img/Long/cropped_face_1.jpg')
    query_image = cv2.cvtColor(query_image, cv2.COLOR_BGR2RGB)
    # plot the query image
    print('Query Image')
    plt.imshow(query_image)


    ranked_list, scores = vit.reference(query_image, data_images_preprocessed)
    print("Ranked list:", ranked_list)
    print("Scores:", scores)
    vit.visualize(query_image, data_images_preprocessed)
