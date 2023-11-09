import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import os

import pyttsx3
import time
import threading

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()



def threadfunc(text):
    t1 = threading.Thread(target=speak(text))
    t1.start()


import pandas as pd
import tensorflow as tf
import os
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm


from keras import layers,callbacks,utils,applications,optimizers
from keras.models import Sequential, Model, load_model
ckp_path=r"D:\mini_project\hand_gesture\archive_"
model=Sequential()


path="C:\\Users\\SANGEETHA S K\\OneDrive\\Desktop\\hand_gesture\\archive_\\enlarged"
files=os.listdir(path)
# list of files in path
# sort path from A-Y
files.sort()
print(files)


interpreter = tf.lite.Interpreter(model_path=r"D:\mini_project\Essential\Essential\model_v2_gesture.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 40
value = 0


def predict():
    global value
    while True:
        success, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            if aspectRatio > 1:

                try:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize

                    imgWhite = cv2.cvtColor(imgWhite, cv2.COLOR_BGR2RGB)
                    imgWhite = np.array(imgWhite, dtype=np.float32)
                    imgWhite = imgWhite.reshape(1, 40, 40, 3)

                    interpreter.set_tensor(input_details[0]['index'], imgWhite)
                    interpreter.invoke()
                    output_data = interpreter.get_tensor(output_details[0]['index'])
                    value = output_data[0][0]
                    value = int(value)

                    # prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    # print(prediction, index)
                except Exception as e:
                    print(str(e))

            else:

                try:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                    imgWhite = cv2.cvtColor(imgWhite, cv2.COLOR_BGR2RGB)
                    imgWhite = np.array(imgWhite, dtype=np.float32)
                    imgWhite = imgWhite.reshape(1, 40, 40, 3)

                    interpreter.set_tensor(input_details[0]['index'], imgWhite)
                    interpreter.invoke()
                    output_data = interpreter.get_tensor(output_details[0]['index'])
                    value = output_data[0][0]
                    value = int(value)

                    # prediction, index = classifier.getPrediction(imgWhite, draw=False)
                except Exception as e:
                    print(str(e))

            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                          (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
            #cv2.putText(imgOutput, files[value], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.putText(imgOutput,files[int[value]], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (255, 0, 255), 4)
        #print(value)
        #print(files[value])


        # engine.say(files[value-1])
        # engine.runAndWait()
        # threadfunc(files[value])

        # cv2.imshow("ImageCrop", imgCrop)
        # cv2.imshow("ImageWhite", imgWhite)

        cv2.imshow("Image", imgOutput)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):

            cap.release()
            cv2.destroyAllWindows()
            for i in range(5):  # maybe 5 or more
                cv2.waitKey(1)
            break


predict()