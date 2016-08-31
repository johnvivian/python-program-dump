#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def detect(img,cascade):
    rects = cascade.detectMultiScale(img,scaleFactor=1.3,minNeighbors=4,minSize=(30,30),flags=cv.CV_HAAR_SCALE_IMAGE)
                       
    if len(rects)==0:
        return []
    rects[:,2:]+=rects[:,:2]
    return rects

def noofpersons(rects):
    return len(rects)
                                    
def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                                    
                                    
if __name__ == '__main__':
   face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
                                    
   camera = PiCamera()
   camera.resolution = (640, 480)
   camera.framerate = 32
   rawCapture = PiRGBArray(camera,size=(640,480))
                                    
   time.sleep(1)
                                    
   for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
       img = frame.array
       img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       img_gray = cv2.equalizeHist(img_gray)
       rawCapture.truncate(0)
             
       rect = detect(img_gray,face_cascade)
           
       print noofpersons(rect)
  
       if rect != [] :
        draw_rects(img,rect,(0,255,0))
       
       cv2.imshow('face',img)                             
                   
       if 0xFF & cv2.waitKey(5) == 27:
          break
        
   cv2.destroyAllWindows()
   camera.close()                                
        
        
                                    
