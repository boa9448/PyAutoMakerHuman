import os
import cv2


dataset_path = os.path.join("dataset", "hand")
img_path_list = []

for root, dirs, files in os.walk(dataset_path):
    for file in files:
        img_path_list.append(os.path.join(root, file))


img_list = (cv2.imread(img_path) for img_path in img_path_list)

for img_path, img in zip(img_path_list, img_list):