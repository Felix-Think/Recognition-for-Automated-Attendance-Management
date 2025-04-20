import kagglehub

# Download latest version
path = kagglehub.dataset_download("dimarodionov/vggface2")

print("Path to dataset files:", path)

#|%%--%%| <k3vloWPpYU|9BPOODgQ4U>


# Tạo thư mục mới (sửa lỗi thiếu khoảng trắng sau -p)
# Tạo thư mục đích
!mkdir -p ./vggface2

# Copy bằng cp (không có progress)
!cp -r /home/felix/.cache/kagglehub/datasets/dimarodionov/vggface2/* ./vggface2/
