import cv2
import numpy as np
from numpy.core.fromnumeric import shape

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",23,255,empty)
cv2.createTrackbar("Threshold2","Parameters",20,255,empty)
cv2.createTrackbar("Area","Parameters",5000,30000,empty)

shape = ''

while True:
    success, img = cap.read()
    # img = img_[150:420, 100:520]
    img = cv2.resize(img,(frameWidth,frameHeight))
    imgContour = img.copy()
    
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        c = max(contours, key=cv2.contourArea)
        print(area)
        if 1000 < area < 8000:
            cv2.drawContours(img, cnt, -1, (255, 0, 255), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            
            x , y , w, h = cv2.boundingRect(approx)
            ar = w / float(h)
            ((x_, y_), radius) = cv2.minEnclosingCircle(c)

            cv2.circle(img, (int(x_), int(y_)), int(radius), (0,255,0), 2)

            if len(approx) == 3:
                cv2.putText(img, "Shape: " + str('Triangle'), (50,50), cv2.FONT_HERSHEY_COMPLEX, .7,
                    (0, 255, 0), 2)
            elif len(approx) == 4:
                cv2.putText(img, "Shape: " + str('Square'), (50,50), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            elif len(approx) == 6:
                cv2.putText(img, "Shape: " + str('Hexagon'), (50,50), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            else:
                cv2.putText(img, "Shape: " + str('Circle'), (50,50), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
            
            dcxx=int(y_*(-0.6989)+769.34)
            dcyy=int(x_*(-0.6805)+219.68)
            
            print("dcxx:",dcxx,"dcyy:",dcyy)
            
            cv2.putText(img, "X coordinates: " + str(dcxx), (400,50), cv2.FONT_HERSHEY_COMPLEX, .5,
                                (0,0,0), 1)
            cv2.putText(img, "Y coordinates: " + str(dcyy), (400,100), cv2.FONT_HERSHEY_COMPLEX, .5,
                                (0,0,0), 1)
    
    cv2.imshow("IMG", img)
    cv2.imshow("Canny",imgCanny)
    cv2.imshow("Dilute",imgDil)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
