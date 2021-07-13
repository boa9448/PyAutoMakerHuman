import env
import cv2
import numpy as np
import imutils
import os
import PyAutoMakerHuman as pamh
import random

dataset_path = os.path.join("dataset", "face")


face = pamh.FaceUtil(min_detection_confidence=0.7)
face.initExtractor()
data = face.extract_dataset(dataset_path)
train_data, name = data["data"], data["name"]

trainer = pamh.SvmUtil()
trainer.train_svm(train_data, name)

#save load test
trainer.load_svm(".")

color_dict = {}
cap = cv2.VideoCapture(0)
while cap.isOpened():
    try:
        success, img = cap.read()
        if not success:
            continue

        img = imutils.resize(cv2.flip(img, 1), width=600)
        data_list = face.extract(img)

        if not data_list:
            cv2.imshow("view", img)
            if cv2.waitKey(1) == ord('q'):
                break

            continue

        for idx, data in enumerate(data_list):
            name, proba = trainer.predict([data[-1]])
            
            if proba < 0.9:
                continue

            box = data[0]
            color = (0, 0, 0)

            if name in color_dict:
                color = color_dict[name]
            else:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                color_dict[name] = color

            cv2.putText(img, f"{name} : {proba:.2f}", (box[0], box[1] - 25)
                        , cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
            cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3])
                            , color, 2)

        cv2.imshow("view", img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    except KeyboardInterrupt:
        break
    except:
        pass
    
cv2.destroyAllWindows()