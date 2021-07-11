import env
import cv2
import imutils
import os
import PyAutoMakerHuman as pamh
import random

dataset_path = os.path.join("dataset", "hand")


hand = pamh.HandUtil(min_detection_confidence=0.7)
hand.initExtractor()
data = hand.extract_dataset(dataset_path)
train_data, name = data["data"], data["name"]

trainer = pamh.SvmUtil()
trainer.train_svm(train_data, name)


cap = cv2.VideoCapture(0)
color_dict = {}
while cap.isOpened():
    success, img = cap.read()
    img = imutils.resize(img, width=600)
    emb_list = hand.extract(img)

    for idx, emb in enumerate(emb_list):
        name, proba = trainer.predict([emb[-1]])
        
        box = emb[0]
        color = (0, 0, 0)

        if name in color_dict:
            color = color_dict[name]
        else:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            color_dict[name] = color


        cv2.putText(img, f"{name} : {proba:.2f}", (box[0], box[1] - 50)
                    , cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3])
                        , color, 2)

    cv2.imshow("view", img)
    cv2.waitKey(1)
    
cv2.destroyAllWindows()