from django.shortcuts import render, HttpResponseRedirect, redirect
import cv2
import numpy as np
import tensorflow as tf
import os
from django.contrib.auth.decorators import login_required
from datetime import datetime
from fer_stats.models import Record
import pytz


ikt_timezone = pytz.timezone('Asia/Irkutsk')

model = tf.keras.models.load_model("emotion_recognition/fer_model/facial_emotion_rec.h5")

haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


class VideoCamera(object):

    def __init__(self, req):
        self.req = req
        self.cap = cv2.VideoCapture(0)

        self.i = 0
        self.fer_counter = [0, 0, 0, 0, 0, 0, 0]

    def __del__(self):
        self.cap.release()

    def get_frame(self):

        ret, frame = self.cap.read()

        gray_im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces_detected = haar_cascade.detectMultiScale(gray_im, 1.32, 5)

        for (x, y, w, h) in faces_detected:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray_im[y:y + w, x:x + h]
            img_pixels = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)

            predictions = model.predict(img_pixels)
            # print(predictions)
            max_index = np.argmax(predictions[0])
            emotions = ('angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise')
            predicted_emotion = emotions[max_index]

            # Расчет эмоции и запись в базу данных
            self.i += 1
            self.fer_counter[max_index] += 1
            print(self.i)
            if self.i == 30:  # примерно 3 секунды
                print(emotions[np.argmax(self.fer_counter)])
                if np.argmax(self.fer_counter) != 4:  # не нейтрально
                    Record.objects.create(
                        date_time=datetime.now(tz=ikt_timezone),
                        emotion_id=np.argmax(self.fer_counter) + 1,
                        user_id=self.req.user.pk
                    )
                self.i = 0
                self.fer_counter = [0, 0, 0, 0, 0, 0, 0]
            cv2.putText(frame, predicted_emotion, (int(x), int(y) - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
