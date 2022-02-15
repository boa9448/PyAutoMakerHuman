# PyAutoMakerHuman
사람과 관련된 자동화 모듈


# 설치
pip install PyAutoMakerHuman

또는

git clone https://github.com/boa9448/PyAutoMakerHuman.git  
cd PyAutoMakerHuman  
python setup.py install  


# 사용

데이터셋 폴더 구조

    dataset
    ├─face
    └─hand
        ├─paper
        ├─rock
        └─scissors



분류기 학습

    import os
    import PyAutoMakerHuman as pamh

    #데이터셋 경로 지정
    dataset_path = os.path.join("dataset", "hand")

    #손 검출 임계치 0.7
    hand = pamh.HandUtil(min_detection_confidence=0.7)

    #데이터셋의 경로를 넘겨주면 사전형 값을 리턴함
    data = hand.extract_dataset(dataset_path)
    train_data, name = data["data"], data["name"]

    trainer = pamh.SvmUtil()
    #svm 학습
    trainer.train_svm(train_data, name)

    #학습된 svm 모델을 myModel폴더에 저장
    trainer.save_svm("myModel")
    


이미지에서 손모양 분류

    import cv2
    import imutils
    import os
    import PyAutoMakerHuman as pamh
    import random

    hand = pamh.HandUtil(min_detection_confidence=0.7)
    trainer = pamh.SvmUtil()

    #학습된 svm모델을 불러옴
    #myModel폴더에 있는 모델과 라벨을 불러옴
    trainer.load_svm("myModel")

    #이미지를 읽어옴
    img_path = "test.jpg"
    img = cv2.imread(img_path)

    #이미지 리사이즈
    img = imutils.resize(img, width=600)
    #이미지에서 박스와 랜드마크를 추출함
    data_list = hand.extract(img)

    color_dict = {}
    #이미지에서 탐지를 성공했다면...
    if data_list:
        for idx, data in enumerate(data_list):
            landmark_1d = data[1]
            name, proba = trainer.predict([landmark_1d])

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
    cv2.waitKey()
    cv2.destroyAllWindows()


# 추후 개발
간단하게 모델을 학습 시킬 수 있는 GUI도구


# GUI도구 미리 둘러보기
패키지 설치 후 
python -m PyAutoMakerHuman
