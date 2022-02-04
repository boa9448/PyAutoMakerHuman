import os
import sys

cur_dir = os.path.dirname(__file__)
lib_dir = os.path.join(cur_dir, "..", "src")
lib_dir = os.path.abspath(lib_dir)

sys.path.append(lib_dir)


from PyAutoMakerHuman import hand
from PyAutoMakerHuman import train
import cv2

dataset_dir = os.path.join(cur_dir, "..", "dataset")
dataset_dir = os.path.abspath(dataset_dir)

util = hand.HandUtil()
dataset = util.extract_dataset(dataset_dir)

trainer = train.SvmUtil()

labels, datas = dataset.values()
trainer.train_svm(datas, labels)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    try:
        success, frame = cap.read()
        if not success:
            continue
        
        data = util.extract(frame)
        if data:
            _, box, data = data[0]
            name, proba = trainer.predict([data])

            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)

        cv2.imshow("result", frame)
        cv2.waitKey(1)


    except KeyboardInterrupt as e:
        break


cap.release()
cv2.destroyAllWindows()

