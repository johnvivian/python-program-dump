import glob
import os
import sys
import numpy
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX =raw_input('Enter The Name')
POSITIVE_DIR ='./training/positive/'+POSITIVE_FILE_PREFIX

def detect_single(image):
	faces = face_cascade.detectMultiScale(image, 1.3, 5)
	if len(faces) != 1:
		return None
	return faces[0]


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
		POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].jpg')))
	count = 0
	if len(files) > 0:
		# Grab the count from the last filename.
		count = int(files[-1][-7:-4])+1
	print 'Capturing positive training images.'
	print 'Press button or type c (and press enter) to capture an image.'
	print 'Press Ctrl-C to quit.'
        a=raw_input()
	while True:
		a=raw_input('Type c (and press enter) to capture an image.\n'"Press Ctrl-C to quit.")
		if is_letter_input(a):
			print 'Capturing image...'
			ret, image = camera.read()
			# Convert image to grayscale.
			image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
			# Get coordinates of single face in captured image.
			result = detect_single(image)
			if result is None:
				print 'Could not detect single face!  Check the image in capture.pgm' \
					  ' to see what was captured and try again with only one face visible.'
				continue
			x, y, w, h = result
			# Crop image as close as possible to desired face aspect ratio.
			# Might be smaller if face is near edge of image.
						# Save image to file.
			filename = os.path.join(POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.jpg' % count)
			cv2.imwrite(filename, image[y+20:y+h+20, x-10:x+w+10])
			print 'Found face and wrote training image', filename
			count += 1