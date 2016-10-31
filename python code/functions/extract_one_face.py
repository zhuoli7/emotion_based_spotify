import numpy as np
import cv2

def detect_target_faces():

	face_img = cv2.imread('face.jpg') 
	face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

	faceDet = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	faceDet2 = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
	faceDet3 = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
	faceDet4 = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")

	face = faceDet.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
	face2 = faceDet2.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
	face3 = faceDet3.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
	face4 = faceDet4.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

	if len(face) == 1:
	    facefeature = face
	elif len(face2) == 1:
	    facefeature == face2
	elif len(face3) == 1:
	    facefeature = face3
	elif len(face4) == 1:
	    facefeature = face4
	else:
	    print('no face detected!')
	    facefeature = ''

	for (x, y, w, h) in facefeature: 

	    cut = face_gray[y:y+h, x:x+w]
	    
	    if (facefeature != ''):
	        extr_face = cv2.resize(cut, (350, 350))
	        cv2.imwrite("face_extracted.jpg", extr_face)
	    else:
	        pass 

def main():
	detect_target_faces()

if __name__ == '__main__':
	main()