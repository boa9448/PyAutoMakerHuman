import env
import cv2
import imutils
import os
import PyAutoMakerHuman as pamh

img_path = "C:\\adrian.jpg"
dataset_path = os.path.join("dataset", "face")


face = pamh.FaceUtil(min_detection_confidence=0.7)
data = face.extract_dataset(dataset_path)
embed, name = data["data"], data["name"]

trainer = pamh.SvmUtil()
trainer.train_svm(embed, name)

img = cv2.imread(img_path)
img = imutils.resize(img, width=600)
emb_list = face.extract(img)

color_list = [(0, 255, 0), (255, 0, 0)]
for idx, emb in enumerate(emb_list):
    result = trainer.predict([emb[-1]])
    print(result)

    cv2.rectangle(img, (emb[0][0], emb[0][1]), (emb[0][0] + emb[0][2], emb[0][1] + emb[0][3]), color_list[idx], 2)

cv2.imshow("view", img)
cv2.waitKey()
cv2.destroyAllWindows()