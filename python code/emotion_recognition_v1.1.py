import cv2
import numpy as np
import glob
import random

emotions = ["neutrality", "anger", "fear", "happiness", "sadness", "surprise"]
fishface = cv2.face.createFisherFaceRecognizer() 
eigenface = cv2.face.createEigenFaceRecognizer()
LBPface = cv2.face.createLBPHFaceRecognizer()

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
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    face_gray = clahe.apply(face_gray)

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
'''
def get_files(emo): 
    trai_set = glob.glob("dataset\\%s\\*" %emo)
    return trai_set

def make_sets():
    trai_data = []
    trai_label = []
    for e in emotions:
        trai_img = get_files(e)
        for i in trai_img:
            image = cv2.imread(i)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            trai_data.append(gray)
            trai_label.append(emotions.index(e))

    return trai_data, trai_label
'''
def recognition():
    '''
    trai_data, trai_label = make_sets()
    '''
    face_img = cv2.imread('face_extracted.jpg') 
    face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    '''
    fishface.train(trai_data, np.asarray(trai_label))
    fishface.save('fishface_mode.XML')
    '''
    fishface.load('fishface_mode.XML')
    #eigenface.load('eigenface_mode.XML')
    #LBPface.load('LBPface_mode.XML')

    res_index = fishface.predict(face_gray)
    res_exp1 = emotions[res_index]
    #res_index = eigenface.predict(face_gray)

    #res_exp2 = emotions[res_index]
    #res_index = LBPface.predict(face_gray)
    #res_exp3 = emotions[res_index]
    return res_exp1
    #return res_exp3

def main():
    
    PhoCap()
    flag = detect_target_faces()
    if(flag==0):
        exp1 = recognition()
        #exp3 = recognition()
        print('This is a face of',exp1)
        #print('This is a face of',exp2)
        #print('This is a face of',exp3)

if __name__ == '__main__':
    main()