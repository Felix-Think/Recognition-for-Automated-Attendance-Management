import os, cv2
import numpy as np
from PIL import Image
def TrainImage(trainimage_path, trainimagelabel_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Id = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(Id))
    recognizer.save(trainimagelabel_path)
    #Add message


def getImagesAndLables(path):
    #GetImagePaths
    newdir = [os.path.join(path, d) for d in os.listdir(path)]
    imagePaths = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        for f in os.listdir(newdir[i])
    ]
    faces = []
    Ids = []
    #Return faces and ID
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath)
        imageNp = np.array(pilImage, "uint8")
        Id = int(os.path.split(imagePath)[-1].split("_")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids
