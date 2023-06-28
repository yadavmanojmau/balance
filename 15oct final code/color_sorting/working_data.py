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

cap = cv2.VideoCapture(1)

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

        if start[0] == 0:
            end = 0
            print("Updating entry value")
        while start[0] == 1 and end == 0:

            print("Capturing Image..")

            GRIP = c.write_single_register(GRIP_addr, 10)
            if end == 0:
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
                        lower_green = np.array([63,109,0])
                        upper_green = np.array([179,255,255])
                        green_mask = cv2.inRange(white_hsv, lower_green, upper_green)
                        green_res = cv2.bitwise_and(white_frame,white_frame, mask= green_mask)
                
                        green_contours, green_hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                        for g_cont in green_contours:
                            
                            green_area = cv2.contourArea(g_cont)
                            c_ = max(green_contours, key=cv2.contourArea)

                            if green_area > 1200 and green_area < 6500:                
                                # cv2.drawContours(white_frame, g_cont , -1, (0, 0, 255), 2)
                                ((x, y), radius) = cv2.minEnclosingCircle(c_)
            
                                cv2.circle(white_frame, (int(x), int(y)), int(radius), (0,255,0), 5)

                dcxx=int(y*(-0.52)+407.53)
                dcyy=int(x*(-0.59)+204.18)
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

                cv2.imshow("Res",white_frame)
                cv2.imshow("Mask",white_res)
                
                cv2.waitKey(10000) 

                end = 1
                if end == 1:
                    break

            
cv2.destroyAllWindows()