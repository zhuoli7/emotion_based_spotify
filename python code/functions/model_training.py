import cv2
import numpy as np
import cv2.face
import glob
import random

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] 
fishface = cv2.face.createFisherFaceRecognizer() 
eigenface = cv2.face.createEigenFaceRecognizer()
LBPface = cv2.face.createLBPHFaceRecognizer()

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

def recognition():
    
    trai_data, trai_label = make_sets()
    
    face_img = cv2.imread('face_extracted.jpg') 
    face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    
    fishface.train(trai_data, np.asarray(trai_label))
    fishface.save('fishface_mode.XML')
    eigenface.train(trai_data, np.asarray(trai_label))
    eigenface.save('eigenface_mode.XML')
    LBPface.train(trai_data, np.asarray(trai_label))
    LBPface.save('LBPface_mode.XML')
    '''
    fishface.load('fishface_mode.XML')

    res_index = fishface.predict(face_gray)
    res_exp = emotions[res_index]
    return res_exp
    '''
def main():
    
    exp = recognition()

if __name__ == '__main__':
    main()