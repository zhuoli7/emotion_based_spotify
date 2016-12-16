import cv2
import cv2.face
import glob
import random
import numpy as np

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
fishface = cv2.face.createFisherFaceRecognizer() 
eigenface = cv2.face.createEigenFaceRecognizer()
LBPface = cv2.face.createLBPHFaceRecognizer()

data = {}

def get_files(emotion):
    files = glob.glob("dataset/%s/*" %emotion)
    random.shuffle(files)
    training = files[:int(len(files)*0.8)] 
    prediction = files[-int(len(files)*0.2):]
    return training, prediction

def make_sets():
    training_data = []
    training_labels = []
    prediction_data = []
    prediction_labels = []
    for emotion in emotions:
        training, prediction = get_files(emotion)
        for item in training:
            image = cv2.imread(item) 
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
            training_data.append(gray) 
            training_labels.append(emotions.index(emotion))
    
        for item in prediction: 
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            prediction_data.append(gray)
            prediction_labels.append(emotions.index(emotion))

    return training_data, training_labels, prediction_data, prediction_labels

def run_recognizer():
    training_data, training_labels, prediction_data, prediction_labels = make_sets()
    
    print ('training fisher face classifier')
    print ('size of training set is:', len(training_labels), "images")
    fishface.train(training_data, np.asarray(training_labels))
    eigenface.train(training_data, np.asarray(training_labels))
    LBPface.train(training_data, np.asarray(training_labels))

    print ("predicting classification set")
    cnt = 0
    correct = 0
    incorrect = 0
    for image in prediction_data:
        pred = fishface.predict(image)
        if pred == prediction_labels[cnt]:
            correct += 1
            cnt += 1
        else:
            incorrect += 1
            cnt += 1
    res = ((100*correct)/(correct + incorrect))
    
    cnt2 = 0
    correct2 = 0
    incorrect2 = 0
    for image in prediction_data:
        pred2 = eigenface.predict(image)
        if pred2 == prediction_labels[cnt2]:
            correct2 += 1
            cnt2 += 1
        else:
            incorrect2 += 1
            cnt2 += 1
    res2 = ((100*correct2)/(correct2 + incorrect2))

    cnt3 = 0
    correct3 = 0
    incorrect3 = 0
    for image in prediction_data:
        pred3 = LBPface.predict(image)
        if pred3 == prediction_labels[cnt3]:
            correct3 += 1
            cnt3 += 1
        else:
            incorrect3 += 1
            cnt3 += 1
    res3 = ((100*correct3)/(correct3 + incorrect3))
    
    return res, res2, res3


score1 = []
score2 = []
score3 = []
for i in range(0,10):
    cor1,cor2, cor3 = run_recognizer()

    print ("got", cor1, "percent correct!")
    print ("got", cor2, "percent correct!")
    print ("got", cor3, "percent correct!")
    score1.append(cor1)
    score2.append(cor2)
    score3.append(cor3)

print ("/n/nend score:", np.mean(score1), "percent correct!")
print ("/n/nend score:", np.mean(score2), "percent correct!")
print ("/n/nend score:", np.mean(score3), "percent correct!")
