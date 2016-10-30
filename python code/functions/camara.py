import cv2
 
def PhoCap():
    cap=cv2.VideoCapture(0)
     
    while True:
        ret,photo=cap.read()
        cv2.imshow('Please Take Photo',photo)
     
        key=cv2.waitKey(2)
     
        if key==ord('\r'):
            filename = "face.jpg"
            cv2.imwrite(filename,photo)
     
        if key==ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    PhoCap()