import glob
import numpy as np
import math
import cv2
import dlib
import pickle
from sklearn.svm import SVC

emotions = ["anger", "fear", "happy", "neutral", "sadness", "surprise"] 
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") 
classifier = SVC(kernel='linear', probability=True, tol=1e-3)


def face_landmark(image):

    detections = detector(image, 1)
    if (len(detections) == 1): 
        for d in detections:
            dot = predictor(image, d)
            list_x = []
            list_y = []
            for i in range(1,68):
                list_x.append(float(dot.part(i).x))
                list_y.append(float(dot.part(i).y))
                
            mean_x = np.mean(list_x)
            mean_y = np.mean(list_y)
            central_x = [(x-mean_x) for x in list_x]
            central_y = [(y-mean_y) for y in list_y]

            if list_x[26] == list_x[29]:
                angle_offset = 0
            else:
                angle_offset = int(math.atan((list_y[26]-list_y[29])/(list_x[26]-list_x[29]))*180/math.pi)

            if angle_offset < 0:
                angle_offset += 90
            else:
                angle_offset -= 90

            land_vector = []
            for x, y, w, z in zip(central_x, central_y, list_x, list_y):
                land_vector.append(x)
                land_vector.append(y)
                meannp = np.asarray((mean_y,mean_x))
                coornp = np.asarray((z,w))
                dist = np.linalg.norm(coornp-meannp)
                if ((w-mean_x) == 0):
                    anglerelative = 90 - angle_offset
                else:
                	anglerelative = (math.atan((z-mean_y)/(w-mean_x))*180/math.pi) - angle_offset
                land_vector.append(dist)
                land_vector.append(anglerelative)

    if len(detections) < 1: 
        print("no face detected")
        land_vector = "error"

    if len(detections) < 1: 
        print("more than one face detected")
        land_vector = "error"

    return land_vector

def data_extr():

    training_data = []
    training_labels = []

    for emotion in emotions:
        training = glob.glob("dataset\\%s\\*" %emotion)
       
        for item in training:
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            clahe_image = clahe.apply(gray)
            land_vector = face_landmark(clahe_image)
            if land_vector == "error":
                pass
            else:
                training_data.append(land_vector)
                training_labels.append(emotions.index(emotion))
                #print(emotion)

    return training_data, training_labels

def main():

    training_data, training_labels= data_extr()

    npar_train = np.array(training_data)
    npar_trainlabs = np.array(training_labels)
    cla = classifier.fit(npar_train, training_labels)
    #print(npar_trainlabs)

    with open('landmark_classifier_alt_less.pkl', 'wb') as file:
        pickle.dump(cla, file)   

    #with open('landmark_classifier.pkl', 'rb') as file:
    #    cla = pickle.load(file)

if __name__ == '__main__':
    main()