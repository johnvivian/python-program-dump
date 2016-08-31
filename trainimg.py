import fnmatch
import os

import cv2
import numpy as np



POSITIVE_LABEL = 1
NEGATIVE_LABEL = 0

NEGATIVE_DIR = './training/negative'
POSITIVE_DIR = './training/positive'
POSITIVE_FILE_PREFIX = 'positive_'

FACE_WIDTH  = 92
FACE_HEIGHT = 112

TRAINING_FILE = './training.xml'

MEAN_FILE = 'mean.png'
POSITIVE_EIGENFACE_FILE = 'positive_eigenface.png'
NEGATIVE_EIGENFACE_FILE = 'negative_eigenface.png'

def walk_files_positive(directory, match='*'):
        dict={}
	for root, dirs, files in os.walk(directory):
                file=[]
     		for filename in fnmatch.filter(files, match):
			 file.append(os.path.join(root, filename))
                fol = root[21:]
                if not fol:
                  continue
                dict[int(fol)]=file
        
        return dict  

def prepare_image(filename):
    img=cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    return cv2.resize(img,(FACE_WIDTH, FACE_HEIGHT),interpolation=cv2.INTER_LANCZOS4)


def walk_files(directory, match='*'):
	"""Generator function to iterate through all files in a directory recursively
	which match the given filename match parameter.
	"""
	for root, dirs, files in os.walk(directory):
		for filename in fnmatch.filter(files, match):
			yield os.path.join(root, filename)


def normalize(X, low, high, dtype=None):
	"""Normalizes a given array in X to a value between low and high.
	Adapted from python OpenCV face recognition example at:
	  https://github.com/Itseez/opencv/blob/2.4/samples/python2/facerec_demo.py
	"""
	X = np.asarray(X)
	minX, maxX = np.min(X), np.max(X)
	# normalize to [0...1].
	X = X - float(minX)
	X = X / float((maxX - minX))
	# scale to [low...high].
	X = X * (high-low)
	X = X + low
	if dtype is None:
		return np.asarray(X)
	return np.asarray(X, dtype=dtype)

if __name__ == '__main__':
	print "Reading training images..."
    
	faces = []
	labels = []
	pos_count = 0
	neg_count = 0
    
	# Read all positive images
        dict=walk_files_positive(POSITIVE_DIR,'*.pgm')
        keys=dict.keys()
        values=dict.values()
        
        for person in keys:
	    for filename in values[person-1]:
  	        faces.append(prepare_image(filename))
	        labels.append(person)
	        pos_count += 1
    
	# Read all negative images
	for filename in walk_files(NEGATIVE_DIR, '*.pgm'):
		faces.append(prepare_image(filename))
		labels.append(NEGATIVE_LABEL)
		neg_count += 1

	print 'Read', pos_count, 'positive images and', neg_count, 'negative images.'

	# Train model
	print 'Training model...'
	model = cv2.createEigenFaceRecognizer()
	model.train(np.asarray(faces), np.asarray(labels))

	# Save model results
	model.save(TRAINING_FILE)
	print 'Training data saved to',TRAINING_FILE

	# Save mean and eignface images which summarize the face recognition model.
	mean = model.getMat("mean").reshape(faces[0].shape)
	cv2.imwrite(MEAN_FILE, normalize(mean, 0, 255, dtype=np.uint8))
	eigenvectors = model.getMat("eigenvectors")
	pos_eigenvector = eigenvectors[:,0].reshape(faces[0].shape)
	cv2.imwrite(POSITIVE_EIGENFACE_FILE, normalize(pos_eigenvector, 0, 255, dtype=np.uint8))
	neg_eigenvector = eigenvectors[:,1].reshape(faces[0].shape)
	cv2.imwrite(NEGATIVE_EIGENFACE_FILE, normalize(neg_eigenvector, 0, 255, dtype=np.uint8))
