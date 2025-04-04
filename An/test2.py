import faiss
import numpy as np

label = np.load("train_labels.npy", allow_pickle=True).item()

print(label)
