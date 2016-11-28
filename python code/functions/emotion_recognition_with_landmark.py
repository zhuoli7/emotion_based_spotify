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

def PhoCap():
    cap=cv2.VideoCapture(0)
    
    while True:
        ret,photo=cap.read()
        cv2.imshow('Please Hit Enter to Take Your Photo and Q to Quit!!',photo)
     
        key=cv2.waitKey(2)
    
        if key==ord('\r'):
            filename = "face.jpg"
            cv2.imwrite(filename,photo)
     
        if key==ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

def detect_target_faces():

    flag = 0

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
        facefeature = face2
    elif len(face3) == 1:
        facefeature = face3
    elif len(face4) == 1:
        facefeature = face4
    else:
        print('Sorry, no face detected!')
        flag = 1
        facefeature = ''

    for (x, y, w, h) in facefeature: 

        cut = face_gray[y:y+h, x:x+w]
        
        try:
            extr_face = cv2.resize(cut, (350, 350))
            cv2.imwrite("face_extracted.jpg", extr_face)
            flag = 0
            return flag
        except:
            return flag 

def recognition():

    face_img = cv2.imread('face_extracted.jpg') 
    face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    land_vec = face_landmark(face_gray)
    np_land_vec = np.array(land_vec)
    #print(np_land_vec)
    #print(np.shape(np_land_vec))
    #print(len(np_land_vec))
    np_land_vec = np_land_vec.reshape(1,-1)
    #print(np.shape(np_land_vec))
    with open('landmark_classifier_alt_less.pkl', 'rb') as file:
        cla = pickle.load(file)
    res_index = cla.predict(np_land_vec)

    res_emo = cla.predict_proba(np_land_vec)
    res_exp = emotions[int(res_index)]

    return res_emo, res_exp

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
                    angle = 90 - angle_offset
                else:
                	angle = (math.atan((z-mean_y)/(w-mean_x))*180/math.pi) - angle_offset
                land_vector.append(dist)
                land_vector.append(angle)

    if len(detections) < 1: 
        print("no face detected")
        land_vector = "error"

    if len(detections) < 1: 
        print("more than one face detected")
        land_vector = "error"
        
    return land_vector

def main():
    
    PhoCap()
    flag = detect_target_faces()
    if(flag==0):
        exp, ind = recognition()
        #for i,e in enumerate(emotions):
            #print(e,":",exp[i])
        print(exp)
        print(ind)

if __name__ == '__main__':
    main()