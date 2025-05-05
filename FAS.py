# -*- coding: utf-8 -*-
# @Time : 20-6-9 下午3:06
# @Author : zhuying
# @Company : Minivision
# @File : test.py
# @Software : PyCharm

import os
import cv2
import numpy as np

from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name

class FAS():
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.model_test = AntiSpoofPredict(device_id)
        self.image_cropper = CropImage()
        self.model_dir = "./resources/anti_spoof_models"

    def DetectSpoof(self,face_crop):
        image = cv2.resize(face_crop, (480, 640))
        image_bbox = self.model_test.get_bbox(image)
        prediction = np.zeros((1, 3))
        # sum the prediction from single model's result
        for model_name in os.listdir(self.model_dir):
            h_input, w_input, model_type, scale = parse_model_name(model_name)
            param = {
                "org_img": image,
                "bbox": image_bbox,
                "scale": scale,
                "out_w": w_input,
                "out_h": h_input,
                "crop": True,
            }
            if scale is None:
                param["crop"] = False
            img = self.image_cropper.crop(**param)
            prediction += self.model_test.predict(img, os.path.join(self.model_dir, model_name))
        value = prediction[0][1]/2
        return value
if __name__ == "__main__":
    pass
