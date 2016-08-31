#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


import os
import sys
import glob
import select

# Prefix for positive training image filenames.
POSITIVE_DIR = os.path.join('./training/positive',str(sys.argv[1]))
POSITIVE_FILE_PREFIX = 'positive_'
FACE_WIDTH  = 92
FACE_HEIGHT = 112


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

def is_letter_input(letter):
    # Utility function to check if a specific character is available on stdin.
    # Comparison is case insensitive.
    if select.select([sys.stdin,],[],[],0.0)[0]:
        input_char = sys.stdin.read(1)
        return input_char.lower() == letter.lower()
        return False

def imgNumber(dir,file_pre):
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    files = sorted(glob.glob(os.path.join(dir,file_pre + '[0-9][0-9][0-9].pgm')))
    count = 0
    if len(files) > 0:
        count= int((files[-1][-7:-4]))+1
    return count

def cropimg(image, rect):
    x,y,w,h = rect[0]
    crop_height = int((FACE_HEIGHT / float(FACE_WIDTH)) * w)
    midy = y + h/2
    y1 = max(0, midy-crop_height/2)
    y2 = min(image.shape[0]-1, midy+crop_height/2)
    return image[y1:y2, x:x+w]

                                    
                                    
if __name__ == '__main__':
   face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
                                    
   camera = PiCamera()
   camera.resolution = (640, 480)
   camera.framerate = 32
   rawCapture = PiRGBArray(camera,size=(640,480))
   
   count = imgNumber(POSITIVE_DIR,POSITIVE_FILE_PREFIX)
                                    
   time.sleep(1)
                                    
   for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
       img = frame.array
       img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       img_gray = cv2.equalizeHist(img_gray)
       rawCapture.truncate(0)
             
       rect = detect(img_gray,face_cascade)
       person_count=noofpersons(rect)
  
       if person_count :
        draw_rects(img,rect,(0,255,0))
       
       cv2.imshow('face',img)
       
       if is_letter_input('c'):
           print 'Capturing Imagae...'
           
           if person_count==1:
              filename = os.path.join(POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % (count))
              cv2.imwrite(filename,cropimg(img_gray,rect))
              print 'Face has been written'
              count+=1
           else:
              print 'More than one face is detected'
                  
       if 0xFF & cv2.waitKey(5) == 27:
          break
        
   cv2.destroyAllWindows()
   camera.close()                                
        
        
                                    
