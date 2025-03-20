import numpy as np
from sklearn.model_selection import train_test_split
data = np.load("data_preprocessed.npy")
X = data[:,0:-1]
y = data[:,-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
label = np.array([y_train]).T
dict = {}
for i in range(len(X_train)):
    dict[i] = label[i]
np.save("train_images_preprocessed.npy", X_train)
np.save("train_labels.npy", dict)
np.save("test_images_preprocessed.npy", X_test)
np.save("test_labels.npy", y_test)

