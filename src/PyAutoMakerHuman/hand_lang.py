import os
import time
from glob import glob

import cv2
import numpy as np

from . import hand_train
from . import image
from . import model_dir

class HandLang:
    char_list = []
    add_thresh = 0.5
    input_delay = 1 #다른 단어 입력
    combination_delay = 2 #조합 임계 시간
    double_char_dict = {"ㄱ" : "ㄲ", "ㄷ" : "ㄸ", "ㅂ" : "ㅃ", "ㅅ" : "ㅆ", "ㅈ" : "ㅉ"}
    combination_char_dict = {hash("ㅗㅏ") : "ㅘ", hash("ㅗㅐ") : "ㅙ", hash("ㅜㅣ") : "ㅟ", hash("ㅜㅓ") : "ㅝ", hash("ㅜㅔ") : "ㅞ"
                            , hash("ㄱㅅ") : "ㄳ", hash("ㄴㅈ") : "ㄵ", hash("ㄴㅎ") : "ㄶ", hash("ㄹㄱ") : "ㄺ"
                            , hash("ㄹㅁ") : "ㄻ", hash("ㄹㅂ") : "ㄼ", hash("ㄹㅅ") : "ㄽ", hash("ㄹㅌ") : "ㄾ"
                            , hash("ㄹㅍ") : "ㄿ", hash("ㄹㅎ") : "ㅀ", hash("ㅂㅅ") : "ㅄ"}


    def __init__(self):
        self.classifier = hand_train.HandTrainer()
        self.classifier.load(model_dir)

    def __del__(self):
        pass

    def set_input_delay(self, delay : float) -> None:
        self.input_delay = delay

    def set_combination_delay(self, delay : float) -> None:
        self.combination_delay = delay

    def set_add_thresh(self, thresh : float) -> None:
        self.add_thresh = thresh

    def add_char(self, cur_time, box, name):
        if self.char_list:
            last_cur_time, last_box, last_name = self.char_list[-1]

            diff_time = cur_time - last_cur_time
            if name == last_name:
                #현재 단어와 이전 단어가 같은 경우
                if diff_time < self.combination_delay:
                    #조합 임계시간을 넘지 않았을 경우
                    x, y, w, h = box
                    last_x, last_y, last_w, last_h = last_box
                    move_range_x, move_range_y = int(w / 2), int(h / 2)
                    move_range = move_range_x if move_range_x < move_range_y else move_range_y

                    center_x, center_y = x + int(w / 2), y + int(h / 2)
                    last_center_x, last_center_y = last_x + int(last_w / 2), last_y + int(last_h / 2)
                    diff_x = abs(center_x - last_center_x)
                    diff_y = abs(center_y - last_center_y)

                    if diff_x > move_range or diff_y > move_range:
                        #중심점이 이동 임계를 넘었다면 추가
                        self.char_list[-1] = (cur_time, box, self.double_char_dict.get(name, name))

                else:
                    #조합 임계시간을 초과했을 경우엔 등록 작업 시작
                    if diff_time > self.input_delay:
                        #입력 시간차이가 입력 임계시간을 초과했을 때만 등록
                        self.char_list.append((cur_time, box, name))

            else:
                #현재 단어와 이전 단어가 다른 경우
                combination_char = self.combination_char_dict.get(hash(last_name + name))
                if combination_char and diff_time < self.combination_delay:
                    #조합 가능한 글자가 있는 경우와 조합 임계시간을 넘지 않았을 경우엔 조합
                    self.char_list[-1] = (cur_time, box, combination_char)

                else:
                    #조합 가능한 글자가 없거나 조합 임계시간을 초과했을 경우는 등록 작업 시작
                    if diff_time > self.input_delay:
                        self.char_list.append((cur_time, box, name))
                    
        else:
            self.char_list.append((cur_time, box, name))

    def get_str(self) -> str:
        name_list = [name for t, box, name in self.char_list]
        return "".join(name_list)

    def remove_char(self, count : int or None = None) -> list:
        if count is None:
            self.char_list.clear()
        else:
            self.char_list = self.char_list[:-count]

    def predict(self, img : np.ndarray) -> list:
        return self.classifier.predict(img)

    def predict_str(self, img : np.ndarray) -> str:
        cur_time = time.time()
        results = self.classifier.predict(img)
        results = list(filter(lambda x : x[-1] > self.add_thresh, results))
        for hand_label, box, name, proba in results:
            self.add_char(cur_time, box, name)

        return self.get_str()
