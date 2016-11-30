import cv2

a=cv2.imread('face.jpg')
while True:
    cv2.imshow("aaa",a)
    key=cv2.waitKey(2)    
    if(key==ord('q')):
        break

