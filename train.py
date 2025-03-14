import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import torch
from transformers import ViTImageProcessor, ViTForImageClassification
#|%%--%%| <BWGceOoaDt|n2xJgxCjNc>

src_dir = './train_img'

classes = {
    img_class: idx for idx, img_class in enumerate(os.listdir(src_dir))
}
classes

#|%%--%%| <n2xJgxCjNc|YWfX5GZgYQ>

path_images = []
for img_class in os.listdir(src_dir):
    class_dir = os.path.join(src_dir, img_class) # train_img/vinh or train_img/long
    for img in os.listdir(class_dir):
        path_image = os.path.join(class_dir, img)
        path_images.append(path_image)
path_images[:5]
#|%%--%%| <YWfX5GZgYQ|mmbgLnZu4q>

# train_dataset
data = {
    'images': [],
    'labels': []
}

for path_image in path_images:
    img = cv2.imread(path_image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data['images'].append(img)
    data['labels'].append(classes[path_image.split('/')[-2]]) # train_img/vinh/*.jpg, -2 is vinh

plt.imshow(data['images'][0])

#|%%--%%| <mmbgLnZu4q|YKYPSOJluD>
from sklearn.model_selection import train_test_split
train_images, test_images, train_labels, test_labels = train_test_split(
    data['images'],
    data['labels'],
    test_size=0.2,
    random_state=42
)
len(train_images), len(test_images), len(train_labels), len(test_labels)



#|%%--%%| <YKYPSOJluD|hzl9WmLZc4>
# Define Metric
def cosine_similarity(query_vector, src_vectors):
    dot_product = np.dot(
        src_vectors,
        query_vector
    )
    src_norm = np.linalg.norm(src_vectors, axis = 1)
    query_norm = np.linalg.norm(query_vector)
    cosine_similarity = dot_product / (src_norm * query_norm)
    return cosine_similarity
#|%%--%%| <hzl9WmLZc4|sU08t1NA9h>

# Define ranking function
def ranking(
    preprocessed_query_image,
    preprocessed_src_images,
    top_k = 10
):
    scores = cosine_similarity(
        preprocessed_query_image,
        preprocessed_src_images
    )

    ranked_list = np.argsort(scores)[::-1][:top_k]
    scores = scores[ranked_list]
    return ranked_list, scores

#|%%--%%| <sU08t1NA9h|jfYFqXtFWS>

#Define preprocessing  function
def preprocessing(images):
    if isinstance(images, list):
        inputs = processor(images, return_tensors='pt').to(device)
    else:
        inputs = processor(images, return_tensors='pt').to(device)

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True).hidden_states[-1][:, 0, :].detach().cpu().numpy()
    return outputs

#|%%--%%| <jfYFqXtFWS|kH7dCjvfYN>

def ranking(preprocessed_query_image, preprocessed_src_images, top_k=10):
    scores = cosine_similarity(preprocessed_query_image, preprocessed_src_images)
    ranked_list = np.argsort(scores)[::-1][:top_k]
    scores = scores[ranked_list]
    return ranked_list, scores
     
#|%%--%%| <kH7dCjvfYN|tbW8fLEFmD>


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224').to(device)

#|%%--%%| <tbW8fLEFmD|DblA7hSuh9>

# Preprocess train_images and test_images
train_images_preprocessed = preprocessing(train_images)

train_images_preprocessed.shape
#|%%--%%| <DblA7hSuh9|0za7v7LrkL>


# Preprocess test_images
test_images_preprocessed = preprocessing(test_images)
test_images_preprocessed.shape



#|%%--%%| <0za7v7LrkL|fYlFM00dTN>


# accuracy
top_k = 5
test_image_preprocessed = test_images_preprocessed[0]
test_label = test_labels[0]

ranked_list, scores = ranking(test_image, train_images_preprocessed, top_k=top_k)

print('Query Image')
query_image = test_images[0]

plt.figure(figsize=(3, 3))
plt.imshow(query_image)
plt.axis('off')
plt.show()

print(f'Top {top_k} similar images')
for idx in range(len(ranked_list)):

    src_image_idx = ranked_list[idx]
    similarity_score = scores[idx]
    plt.figure(figsize=(3, 3))
    plt.imshow(train_images[src_image_idx])
    plt.title(f'Similarity: {similarity_score:.10f}')
    plt.axis('off')
    plt.show()

#|%%--%%| <fYlFM00dTN|ue7SneVgqt>

# Luu file npoy

np.save('train_images_preprocessed.npy', train_images_preprocessed)
np.save('test_images_preprocessed.npy', test_images_preprocessed)
