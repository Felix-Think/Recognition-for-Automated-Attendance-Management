import faiss
import numpy as np

dim  = 768
# ---Register Data---
register = np.load("train_images_preprocessed.npy")

# --- Tạo Quantizer và IndexIVFPQ ---
quantizer = faiss.IndexFlatL2(dim)
nlist = 2   # Số lượng phân vùng
m = 16         # Số lượng subquantizer (mỗi vector sẽ được chia thành m phần)
nbits = 1    # Số bit cho mỗi subvector
index_ivfpq = faiss.IndexIVFPQ(quantizer, dim, nlist, m, nbits)
# --- Huấn luyện index ---
index_ivfpq.train(register)
# Output: True
index_ivfpq.add(register)
print("Total number of vectors:", index_ivfpq.ntotal)

# --- Truy vấn ---
k = 5
X_test = np.load("test_images_preprocessed.npy")
y_test = np.load("test_labels.npy")
D, I = index_ivfpq.search(X_test, k)
label_dict = np.load("train_labels.npy", allow_pickle=True).item()
# --- Tính độ chính xác ---
# Optimize the query process using numpy
def lookup(key,my_dict):
    return my_dict.get(key, "Không tìm thấy")

# Vectorize hàm lookup
vectorized_lookup = np.vectorize(lookup)
y_pred = np.array([])
for i in np.arange(I.shape[0]):
    topk_pred = vectorized_lookup(I[i],label_dict)
    unique, counts = np.unique(topk_pred, return_counts=True)
    y_pred = np.append(y_pred,unique[np.argmax(counts)])
y_pred = np.array(y_pred)
accuracy = np.mean(y_pred == y_test)
print("Accuracy:", accuracy)