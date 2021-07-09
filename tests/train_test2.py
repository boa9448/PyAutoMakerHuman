import env
import cv2
import imutils
import os
import PyAutoMakerHuman as pamh

img_path = "C:\\adrian.jpg"
dataset_path = "dataset"


face = pamh.FaceUtil(min_detection_confidence=0.7)
face.initExtractor()
data = face.extract_dataset(dataset_path)
embed, name = data["embed"], data["name"]

trainer = pamh.SvmUtil()
trainer.train_svm(embed, name)


cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, img = cap.read()
    img = imutils.resize(img, width=600)
    emb_list = face.extract(img)

    color_list = [(0, 255, 0), (255, 0, 0)]
    for idx, emb in enumerate(emb_list):
        result = trainer.predict([emb[-1]])
        print(result)

        cv2.rectangle(img, (emb[0][0], emb[0][1]), (emb[0][0] + emb[0][2], emb[0][1] + emb[0][3]), color_list[idx], 2)

    cv2.imshow("view", img)
    cv2.waitKey(1)
    
cv2.destroyAllWindows()