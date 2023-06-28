import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
global x,y

while True:

    _,white_frame = cap.read()
    white_frame = white_frame[150:350, 200:460]
    white_frame = cv2.resize(white_frame,(640,480)) ### resize the camera output window
    white_hsv = cv2.cvtColor(white_frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0,0,87])
    upper_white = np.array([179,52,255])
    white_mask = cv2.inRange(white_hsv, lower_white, upper_white)
    white_res = cv2.bitwise_and(white_frame,white_frame, mask= white_mask)
    
    white_contours, white_hierarchy = cv2.findContours(white_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for box_c in white_contours:
        box_area = cv2.contourArea(box_c)  ### Get area of the contour detected
        if box_area>50000:          ## Setting the threshold for blue area
            # print(box_area)                       
            cv2.drawContours(white_frame, box_c, -1, (0, 255, 0), 5)  ## Draw contours of blues color
            lower_green = np.array([83,68,0])
            upper_green = np.array([179,255,255])
            green_mask = cv2.inRange(white_hsv, lower_green, upper_green)
            green_res = cv2.bitwise_and(white_frame,white_frame, mask= green_mask)
    
            green_contours, green_hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            for g_cont in green_contours:
                    
                green_area = cv2.contourArea(g_cont)
                c = max(green_contours, key=cv2.contourArea)

                if green_area > 1200 and green_area < 6500:                
                    # cv2.drawContours(white_frame, g_cont , -1, (0, 0, 255), 2)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
   
                    cv2.circle(white_frame, (int(x), int(y)), int(radius), (0,255,0), 5)

    
    dcxx=int(y*(-0.52)+407.53)

    dcyy=int(x*(-0.59)+204.98)

    print(dcxx,dcyy)
    
    cv2.imshow("Res",white_frame)
    cv2.imshow("Mask",white_res)
    cv2.imshow("Greeen_Mask",green_mask)

    cv2.waitKey(30000)
