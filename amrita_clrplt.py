import cv2
import numpy as np
from pyModbusTCP.client import ModbusClient  # for establishing Communication between PLC and PC
#from pyModbusTCP.server import ModbusServer
import time

#cap = cv2.VideoCapture(0)  ## Loading the video

#SERVER_HOST = "192.168.0.12"  # put ip address of plc here
#SERVER_PORT = 502  # port no of plc
c1 = ModbusClient(host="192.168.0.12",port=502,unit_id=1, auto_open=True)  # Create an instance of the Modbus Client and this will be used further
#c.host()
#c.port()

CX_addr = 50  # Coordinates for x_axis
SX_addr = 14  # Sign for x axis

CY_addr = 51  # Coordinates for y_axis
SY_addr = 15  # Sign for y_axis

Colour_addr = 52  # Red =1 ; yellow = 2

CTC_addr = 99  # Acknowledgement bit coming at this address will start the process

done_addr = 13  # To inform the PLC about the finished process
# Colour_addr = 52  # Red =1 ; yellow = 2


end = 0  # Used for flag conditions

# Starting the main operation

print("Attempting to connect to PLC...")

# Checking if the PC and PLC have established connection
# if not c.is_open():
#     if not c.open():
#         print("unable to connect to " + host + ":" + port)

# # Once the PLC and PC are connected
# if c.is_open():
#     print("Done Connecting to PLC...")

cap = cv2.VideoCapture(0)
while True:
    ret, white_frame = cap.read()  ## Reading the frames from Video
    
    white_frame = white_frame[150:350, 200:460]  ### Creating Region of Intrest

    white_frame = cv2.resize(white_frame, (640, 480))  ### resize the camera output window
    cv2.imshow("image", white_frame)
    
    hsv_frame = cv2.cvtColor(white_frame, cv2.COLOR_BGR2HSV)

    # lower_yellow = np.array([18,0,0])   ## Low H,S,V values from trackbar
    # upper_yellow = np.array([68,255,255]) ## High H,S,V values from trackbar

   # lower = {'red': (2, 224, 113)}
   # upper = {'red': (7, 255, 160)}

   # colour = {'red': (0, 0, 255)}  ####hsv value of red yellow
    # lower = {'yellow': (21, 255, 130), 'red': (2, 224, 113)}
    # upper = {'yellow': (28, 255, 186), 'red': (7, 255, 160)}

    # colour = {'yellow': (0, 255, 217), 'red': (0, 0, 255)}  # hsv value of red yellow
    lower = {'yellow': (16, 199, 75), 'red': (0, 142, 62), 'green': (35, 108, 0)}
    upper = {'yellow': (35, 255, 217), 'red': (7, 255, 172), 'green': (179, 255, 255)}

    colour = {'yellow': (0, 255, 217), 'red': (0, 0, 255), 'green': (0, 255, 0)}  # hsv value of red yellow

    '''
        lower - lower hsv range of the colour to be detected
        upper - upper hsv range of the colour to be detected
        colors - RGB values of the color to be detected
    '''

    for key, value in upper.items():

        #print("inside 1st for")

        mask = cv2.inRange(hsv_frame, lower[key], upper[key])
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        '''
        contours: finding outlines
        '''

        for box_c in contours:
            #print("inside 2st for")
            object_area = cv2.contourArea(box_c)  ## find area of the contours of objects detected
            c = max(contours, key=cv2.contourArea)
            if object_area > 10000:
                #print("inside if object_area > 10000: ")

                ((x, y), radius) = cv2.minEnclosingCircle(c)  ## Drawing circles

                M = cv2.moments(c)  ### Get centre of the contours detected
                try:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    if colour[key] == (0, 255, 217):
                        #print("inside if if colour[key] ")
                        '''
                         If the color detected is yellow it will indicate to the arduino so that is 
                         moves the arm accordingly 
                         '''
                        detected_colour = 1
                        print("Detected color is yellow: ")
                        c1.write_single_register(52, 1)
                    #     #c.write_single_register(Colour_addr, 1)
                    #     # print(key)

                    if colour[key] == (0, 0, 255):
                        #print("inside if if colour[key] ")
                        
                        '''
                        If the color detected is red it will indicate to the arduino so that is 
                        moves the arm accordingly 
                        '''
                        detected_colour = 2
                                               
                        #y =12
                        #print(y)
                        print("Detected color is Red: ")
                        #time.sleep(3)
                        c1.write_single_register(52, 2)
       
    
                        #c.write_single_register(52, y)
                    if colour[key] == (0, 255, 0):
                        #print("inside if if colour[key] ")
                        '''
                         If the color detected is yellow it will indicate to the arduino so that is 
                         moves the arm accordingly 
                         '''
                        detected_colour = 3
                        print("Detected color is green: ")
                        c1.write_single_register(52, 3)
                    #     #c.write_single_register(Colour_addr, 1)
                    #     # print(key)    
                        
                        #cap.release()
                        #break
                        # c.write_single_register(52, 2)
                        #c.write_single_register(Colour_addr, 2)
                    
                    if radius > 0.5:
                        cv2.circle(white_frame, (int(x), int(y)), int(radius), colour[key], 5)
                        cv2.putText(white_frame, key + "color", (int(x - radius), int(y - radius)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    colour[key], 2)
                except:
                    pass
    # mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    '''
    inRange: take hsv_frame as input and search for colors of values 
             in range lower_yellow and upper_yellow
    '''
    # yellow_res = cv2.bitwise_and(white_frame,white_frame, mask= mask)

    '''
    bitwise_and: Normal anding operation between white_frame and mask
                created by mask 
    '''

    # yellow_contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    
    # cv2.imshow("resul",yellow_res)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()