import cv2
import cv2.face
import glob
import numpy as np

def get_files(emotion): 
    files = glob.glob("dataset\\%s\\*" %emotion)
    training = files
    return training

def make_sets():
    training_data = []
    training_labels = []
    prediction_data = []
    prediction_labels = []
    for emotion in emotions:
        training = get_files(emotion)

        for item in training:
            image = cv2.imread(item) 
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
            training_data.append(gray)
            training_labels.append(emotions.index(emotion))

        face_img = cv2.imread('face.jpg')
        face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

    return training_data, training_labels