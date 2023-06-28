import cv2
import numpy as np
from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "192.168.0.23"
SERVER_PORT = 502
c = ModbusClient()
c.host(SERVER_HOST)
c.port(SERVER_PORT)

CX_addr=50 #Coordinates for x axis
SX_addr=14 #Sign for x axis
CY_addr=51 #Coordinates for y axis
SY_addr=15 #Sign for y axis
Colour_addr = 52 #green =1 ; blue = 2; red = 3;
Ang_addr = 54 # address for orientation angle
GRIP_addr =101 #Gripper open = 1 and close =0
CTC_addr = 99 #clear to capture
CTCB_addr = 12
done_addr = 13
CTS_addr = 11
end = 0
cap = cv2.VideoCapture(0)

def yellow_detect(frame,hsv):
    
    lower_yellow = np.array([4,90,0])
    upper_yellow = np.array([67,255,255])
    
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_res = cv2.bitwise_and(frame,frame, mask= yellow_mask)

    yellow_contours, green_hierarchy = cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for g_cont in yellow_contours:
        
        yellow_area = cv2.contourArea(g_cont)
        c = max(yellow_contours, key=cv2.contourArea)

        if yellow_area > 1200 and yellow_area < 6500:                
            ((yellow_x, yellow_y), radius) = cv2.minEnclosingCircle(c)

            cv2.circle(frame, (int(yellow_x), int(yellow_y)), int(radius), (0, 255, 217), 5)
    
    cv2.imshow("yellow_mask",yellow_mask)

    if yellow_x != 0:
        return yellow_x,yellow_y
    else:
        return 0,0

def green_detect(frame,hsv):
    
    lower_green = np.array([63,109,0])
    upper_green = np.array([85,255,255])
    
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_res = cv2.bitwise_and(frame,frame, mask= green_mask)
    
    green_contours, green_hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for g_cont in green_contours:
        
        green_area = cv2.contourArea(g_cont)
        c = max(green_contours, key=cv2.contourArea)

        if green_area > 1200 and green_area < 6500:                
            ((green_x, green_y), radius) = cv2.minEnclosingCircle(c)

            cv2.circle(frame, (int(green_x), int(green_y)), int(radius), (0,255,0), 5)

    cv2.imshow("green_mask",green_mask)
    
    if green_x != 0:
        return green_x,green_y
    else:
        return 0,0


###############################################

print("Attempting to connect to PLC...")

if not c.is_open():
    if not c.open():
        print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
if c.is_open():
    print("Done Connecting to PLC...")
    while(1):
        start = c.read_holding_registers(CTC_addr,1)
        print("start: ",start )
        c.write_single_coil(done_addr, 0)

        while start[0] == 1 :
            print("Capturing Image..")

            GRIP = c.write_single_register(GRIP_addr, 10)

            _,frame = cap.read()
            white_frame = frame[150:350, 200:460]
            white_frame = cv2.resize(white_frame,(640,480)) ### resize the camera output window
            white_hsv = cv2.cvtColor(white_frame, cv2.COLOR_BGR2HSV)
            
            y_x,y_y = yellow_detect(white_frame,white_hsv)
            g_x,g_y = green_detect(white_frame,white_hsv)

            print(y_x,y_y)
            print(g_x,g_y)

            X_cord = []
            Y_cord = []

            X_cord.append((y_x,g_x))
            Y_cord.append((y_y,g_y))

            x_to_send = X_cord[0][0]
            y_to_send = Y_cord[0][0]

            print(x_to_send,y_to_send)

            dcxx=int(y_to_send*(0.6171)-131.21)

            dcyy=int(x_to_send*(-0.4526)+484.18)

            print(dcxx,dcyy)

            if dcxx < 0:
                dcxx = (dcxx * (-1))
                c.write_single_coil(SX_addr,1)
            else:
                c.write_single_coil(SX_addr,0)
            if dcyy < 0:
                dcyy = (dcyy * (-1))
                c.write_single_coil(SY_addr,1)
            else:
                c.write_single_coil(SY_addr,0)

            P_CY = c.write_single_register(CX_addr, int(dcxx))
            P_CX = c.write_single_register(CY_addr, int(dcyy))

            c.write_single_register(Colour_addr,1)            
            c.write_single_coil(done_addr, 1)  #added by ad

            cv2.imshow("res",white_frame)

            print("Done Processing")
            cv2.waitKey(0)
cv2.destroyAllWindows()
