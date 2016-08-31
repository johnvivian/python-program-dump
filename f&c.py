import glob
import os
import sys
import select

import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
while 1:
def detect_single(image):
    ret, image = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = image[y:y+h, x:x+w]
    if len(faces) !=   1:
        return None
    return faces[0]
def crop(image, x, y, w, h):
    crop_height = int((112 / float(92)) * w)
    midy = y + h/2
    y1 = max(0, midy-crop_height/2)
    y2 = min(image.shape[0]-1, midy+crop_height/2)
    return image[y1:y2, x:x+w]
def resize(image):
    return cv2.resize(image,(92,112),interpolation=cv2.INTER_LANCZOS4)
cv2.imshow('img',img)
k = cv2.waitKey(30) & 0xff
if k == 27:
    break

cap.release()
cv2.destroyAllWindows()