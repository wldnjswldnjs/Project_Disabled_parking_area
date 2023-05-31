import paho.mqtt.client as mqtt
from threading import Thread, Event
from IPython.display import Image
import paho.mqtt.publish as publish
import os
import subprocess
import time
from datetime import datetime
import os

# 번호판 library
import cv2
import pytesseract
from pytesseract import *
import numpy as np
import os
from glob import glob

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import cv2
import pytesseract
from PIL import Image, ImageChops, ImageEnhance

# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import matplotlib.pyplot as plt
# import numpy as np
# import tensorflow as tf
# import pandas as pd
# from glob import glob

# import efficientnet
# import efficientnet.tfkeras as efn

# from tensorflow.keras.models import Sequential,load_model
# from tensorflow.keras.layers import Dense
# from keras.preprocessing import image

# from tensorflow.keras.layers import GlobalAveragePooling2D
# # import tensorflow_addons as tfkeras
# from tensorflow.keras.callbacks import EarlyStopping

# from tensorflow.keras.optimizers import Adam
# import matplotlib.pyplot as plt
# import cv2 as cv                 # opencv (이미지 resize)

class MqttWorker:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.exit_event = Event()

    def signal_handler(self, signum, frame):
        print("signal_handler===================================")
        self.exit_event.set()  # 이벤트객체가 갖고 있는 플래그 변수가 True로 셋팅
        # 현재 이벤트 발생을 체크하고 다른 작업을 수행하기 위한 코드 - 다른 메소드에서 처리
        if self.exit_event.is_set():
            print("이벤트객체의 플래그변수가 Ture로 바뀜 - 이벤트가 발생하면 어떤 작업을 실행하기 위해서(다른 메소드 내부에서 반복문 빠져나오기~....)")
            exit(0)

    def mymqtt_connect(self):  # 사용자정의 함수 - mqtt서버연결과 쓰레드생성 및 시작을 사용자정의 함수로 정의
        try:
            print("브로커 연결 시작하기")
            self.client.connect("3.25.85.102", 1883, 60)
            mythreadobj = Thread(target=self.client.loop_forever)
            mythreadobj.start()
        except KeyboardInterrupt:
            pass
        finally:
            print("종료")

    def on_connect(self, client, userdata, flags, rc):  # broker접속에 성공하면 자동으로 호출되는 callback함수
        print("connect..." + str(rc))  # rc가 0이면 성공 접속, 1이면 실패
        if rc == 0:  # 연결이 성공하면 구독신청
            client.subscribe("mydata/number")
        else:
            print("연결실패.....")
            # 라즈베리파이가 메시지를 받으면 호출되는 함수이므로 받은 메시지에 대한 처리를 구현

    def on_message(self, client, userdata, message):
        try:
            
            now = datetime.now()
            file_name = now.strftime('%Y-%m-%d-%H:%M:%S')

            print("[", file_name, "(parking sign)]")
            # 이미지 저장
            val_img_path = "/home/lab28/mount/number_img/" + file_name + "_number.jpg"

            f = open(val_img_path, "wb")
            f.write(message.payload)
            f.close()
          
            os.environ['MKL_THREADING_LAYER'] = 'GNU'
            cmd = "python /home/lab28/yolov5_license_plate/detect.py --weights /home/lab28/yolov5_license_plate/best.pt --img 416 --conf 0.5 --source {} --save-conf --save-crop".format(
                val_img_path)
            bashCmd = cmd.split()
            subprocess.Popen(bashCmd).wait(timeout=None)
     
            # 차 번호 Detect
            img = cv2.imread(val_img_path)

            # 회색 변환(channel 수 감소)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 이진수 변환(흑 / 백)
            img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # 모폴로지 연산(Opening)
            kernel = np.ones((5, 5), np.uint8)
            img_open = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)

            # tesseract 설정
            # custom_config = '--oem 3' # LSTM 버전
            text = pytesseract.image_to_string(img, 'eng+Hangul')  # 한글은 kor이 아닌 Hangul
            print(text)

            # detect 하위 dir 경로 및 해당 dir name (concat)
            subfolders = pd.DataFrame(
                [f.path for f in os.scandir('/home/lab28/yolov5_license_plate/runs/detect/') if f.is_dir()],
                columns=['dir_path'])
            subfolders_nm = pd.DataFrame(
                [f.name for f in os.scandir('/home/lab28/yolov5_license_plate/runs/detect/') if f.is_dir()],
                columns=['dir_name'])
            subfolders_frm = pd.concat([subfolders, subfolders_nm], axis=1)

            # checkpoints dir 제거(사용할 최종 data) : sub_exp_frm
            sub_exp_frm = subfolders_frm.loc[~subfolders_frm.dir_name.str.contains('check'), :]

            # exp 뒤의 숫자가 가장 큰 dir 찾기 (가장 최신 detection) : new_dir
            new_idx = sub_exp_frm.dir_name.str[3:].replace('', 0).astype(int).argmax()  # 해당 dir 있는 index number
            new_dir = sub_exp_frm.iloc[new_idx, 0]

            if 'crops' in os.listdir(new_dir):
                for (path, dir, files) in os.walk(new_dir + '/crops/'):
                    for filename in files:
                        ext = os.path.splitext(filename)[-1]
                        if ext == '.jpg':
                            label_nm = path.split('/')[-1]
                            crop_img_path = '%s/%s' % (path, filename)
                            print(label_nm)
                            print(crop_img_path)
                            sign = 1
            else:
                print("No crop image")
                publish.single("web/carnumber", "NULL", hostname="3.25.85.102")
                sign = 0
               

            if (sign == 1) and (label_nm == 'old'):
                print('구 번호판 전처리')
                print(crop_img_path)
                img = cv2.imread(crop_img_path)

                alpha = 4.0  # 명암 조정값
                dst = np.clip((1 + alpha) * img - 128 * alpha, 0, 255).astype(np.uint8)

                # 회색 변환(channel 수 감소)
                img_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

                # 이진수 변환(흑 / 백)
                img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                # 모폴로지 연산(Opening)
                kernel = np.ones((5, 5), np.uint8)
                img_open = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)

                custom_config = '--psm 12 --oem 3'

                car_number = pytesseract.image_to_string(img_binary, 'Hangul+eng+osd', config=custom_config)
                            
                # 메세지 전송
                if len(car_number) == 5:
                    publish.single("web/carnumber", car_number, hostname="3.25.85.102")
                else:
                    publish.single("web/carnumber", "NULL", hostname="3.25.85.102")
                   
            elif (sign == 1) and (label_nm == 'new'):
                print('신 번호판 전처리')
                print(crop_img_path)
                img = cv2.imread(crop_img_path)
                #     img = cv2.imread('/home/lab34/yolov5_license_plate/license_plate_image_raw/ys(2)test.jpg')
                height, width, channel = img.shape

                # 회색 변환(channel 수 감소)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # 이진수 변환(흑 / 백)
                img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                # 모폴로지 연산(Opening)
                kernel = np.ones((5, 5), np.uint8)
                img_open = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)

                custom_config = '--psm 9 --oem 3'  # psm : 0~13 / oem : 0~3

                car_number = pytesseract.image_to_string(img_binary, 'Hangul+eng+osd', config=custom_config)
              
                # 메세지 전송
                if len(car_number) == 5:
                    publish.single("web/carnumber", car_number, hostname="3.25.85.102")
                else:
                    publish.single("web/carnumber", "NULL", hostname="3.25.85.102")
                         
        except:
            pass
        finally:
            pass


if __name__ == '__main__':
    try:
        mqtt = MqttWorker()
        mqtt.mymqtt_connect()  # callback 함수가 아니므로 인스턴스 변수를 이용해서 호출해야 한다.
    except KeyboardInterrupt:
        pass
    finally:
        pass


