import cv2
import numpy as np
import cv2.cv as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


POSITIVE_LABEL = 1
NEGATIVE_LABEL = 2
POSITIVE_THRESHOLD = 5600.0

FACE_WIDTH  = 92
FACE_HEIGHT = 112

TRAINING_FILE = './training.xml'

def detect(img,cascade):
    rects = cascade.detectMultiScale(img,scaleFactor=1.3,minNeighbors=4,minSize=(30,30),flags=cv.CV_HAAR_SCALE_IMAGE)
    
    if len(rects)==0:
        return []
    rects[:,2:]+=rects[:,:2]
    return rects

def noofpersons(rects):
    return len(rects)

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
   
   model = cv2.createEigenFaceRecognizer()
   model.load(TRAINING_FILE)

   time.sleep(1)
                                    
   for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
       img = frame.array
       img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       img_gray = cv2.equalizeHist(img_gray)
       rawCapture.truncate(0)
             
       rect = detect(img_gray,face_cascade)
       person_count=noofpersons(rect)
         
       if person_count==1:
           face=cv2.resize(cropimg(img_gray,rect),(FACE_WIDTH, FACE_HEIGHT),interpolation=cv2.INTER_LANCZOS4)
           label,confidence = model.predict(face)
            
           print [label,confidence]
            
           if confidence < POSITIVE_THRESHOLD:
               if label==1:
                   print 'Recognized face!'
           else:
               print 'Did not recognize face!'

       if 0xFF & cv2.waitKey(5) == 27:
          break
        
   cv2.destroyAllWindows()
   camera.close()
