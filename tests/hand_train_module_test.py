import cv2

import env
from PyAutoMakerHuman.hand import HandResult
from PyAutoMakerHuman.hand_train import HandTrainer
from PyAutoMakerHuman.image import cv2_putText


util = HandTrainer()
#util.train(env.train_dataset_dir)
#util.save("test_model")
util.load("test_model")

cap = cv2.VideoCapture(0)
while cap.isOpened():
    try:
        success, frame = cap.read()
        if not success:
            continue
        
        frame = cv2.flip(frame, 1)
        result = util.predict(frame)
        if result:
            hand_result : HandResult = result[0]
            predict_result = result[1]
            
            boxes = hand_result.get_boxes()
            for (hand_label, box), (name, proba) in zip(boxes, predict_result):
                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame =cv2_putText(frame, f"{hand_label}_{name} __ {proba:0.2f}", (x, y - 15), 3, (0, 0, 255), 2)

        cv2.imshow("view", frame)
        key = cv2.waitKey(1)
        if key & 0xff == ord('q'):
            break

    except KeyboardInterrupt:
        break


cap.release()
cv2.destroyAllWindows()
