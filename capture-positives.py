import glob
import os
import sys
import numpy
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX = 'positive_'
POSITIVE_DIR = './training/positive'

def crop(image, x, y, w, h):
	crop_height = int((112 / float(92)) * w)
	midy = y + h/2
	y1 = max(0, midy-crop_height/2)
	y2 = min(image.shape[0]-1, midy+crop_height/2)
	return image[y1:y2, x:x+w]





def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if letter=='c':
			return True
	return False


if __name__ == '__main__':
	camera =cv2.VideoCapture(0)
		# Create the directory for positive training images if it doesn't exist.
	if not os.path.exists(POSITIVE_DIR):
		os.makedirs(POSITIVE_DIR)
	# Find the largest ID of existing positive images.
	# Start new images after this ID value.
	files = sorted(glob.glob(os.path.join(POSITIVE_DIR,
		POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
	count = 0
	if len(files) > 0:
		# Grab the count from the last filename.
		count = int(files[-1][-7:-4])+1
	print 'Capturing positive training images.'
    while True:
        ret, image = camera.read()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(image, 1.3, 5)

        for (x,y,w,h) in faces:
         cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
         roi_gray = gray[y:y+h, x:x+w]
         roi_color = img[y:y+h, x:x+w]

         if len(faces) != 1:
		    result =None
        else:
            print 'face found'
            result=1
        cv2.imshow('image',image)

	        a=raw_input('Type c (and press enter) to capture an image.\n'"Press Ctrl-C to quit.")

		if  is_letter_input(a):
			print 'Capturing image...'
			if result is None:
				print 'Could not detect single face!'
				continue
						# Crop image as close as possible to desired face aspect ratio.
			# Might be smaller if face is near edge of image.
			# Save image to file.
			filename = os.path.join(POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.jpg' % count)
			img=image
			cv2.imwrite(filename, img)
			print 'Found face and wrote training image', filename
			count +1
camera.release()
cv2.destroyAllWindows()
