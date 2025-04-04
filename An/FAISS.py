import faiss
import numpy as np

class FaissIndexer:
    def __init__(self, d, index_type="IVFPQ", nlist=0, **kwargs):
        """
        Khởi tạo đối tượng FaissIndexer.
        
        :param d: Số chiều của vector.
        :param index_type: Loại index cần dùng. Một số lựa chọn:
                           - "FlatL2": Index cơ bản sử dụng khoảng cách Euclidean.
                           - "IVFFlat": Inverted File với vector gốc (Flat).
                           - "IVFPQ": Inverted File với Product Quantization.
        :param nlist: Số cụm cho index IVF (áp dụng với IVFFlat và IVFPQ).
        :param kwargs: Các tham số bổ sung (ví dụ: m cho IVFPQ).
        """
        self.d = d
        self.index_type = index_type
        self.nlist = nlist
        self.kwargs = kwargs
        self.index = None
        self._init_index()

    def _init_index(self):
        """Khởi tạo index dựa trên loại index được chọn."""
        if self.index_type == "FlatL2":
            self.index = faiss.IndexFlatL2(self.d)
        elif self.index_type == "IVFFlat":
            quantizer = faiss.IndexFlatL2(self.d)
            self.index = faiss.IndexIVFFlat(quantizer, self.d, self.nlist)
        elif self.index_type == "":
            quantizer = faiss.IndexFlatL2(self.d)
            # m là số phần chia cho Product Quantization, mặc định 16 nếu không truyền vào
            m = self.kwargs.get("m", 16)
            self.index = faiss.IndexIVFPQ(quantizer, self.d, self.nlist, m, 1)  # 8 bits cho mỗi sub-vector
        else:
            raise ValueError("Loại index không được hỗ trợ.")

    def train(self, training_vectors):
        """
        Huấn luyện index (nếu cần). Chỉ cần gọi nếu index cần train như IVFFlat, IVFPQ.
        
        :param training_vectors: Ma trận vector dùng để huấn luyện.
        """
        if not self.index.is_trained:
            self.index.train(training_vectors)
            print("Huấn luyện index thành công.")

    def add_vectors(self, vectors):
        """
        Thêm vector vào index.
        
        :param vectors: Ma trận vector cần thêm.
        """
        self.index.add(vectors)
        print(f"Đã thêm {len(vectors)} vector vào index.")

    def search(self, query_vectors, k=5):
        """
        Tìm kiếm k láng giềng gần nhất cho các vector truy vấn.
        
        :param query_vectors: Ma trận vector truy vấn.
        :param k: Số láng giềng gần nhất cần tìm.
        :return: Khoảng cách và chỉ số của các vector gần nhất.
        """
        distances, indices = self.index.search(query_vectors, k)
        return distances, indices

    def save_index(self, filename):
        """
        Lưu index vào file.
        
        :param filename: Tên file để lưu index.
        """
        faiss.write_index(self.index, filename)
        print(f"Index đã được lưu vào file: {filename}")

    def load_index(self, filename):
        """
        Tải index từ file.
        
        :param filename: Tên file chứa index đã lưu.
        """
        self.index = faiss.read_index(filename)
        print(f"Index đã được tải từ file: {filename}")