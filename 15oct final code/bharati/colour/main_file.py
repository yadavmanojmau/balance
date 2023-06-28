#### Import necessary libraries ####
import cv2                                        ####  Computer Vision Library
import numpy as np                                  
from pyModbusTCP.client import ModbusClient       ####  for establishing Communication between PLC and PC
import time

""" 
Capture Frame from the Webcam
0: for 1st camera
1: for 2nd camera
and continue if any more connected
"""
cap = cv2.VideoCapture(0)


### Declare the IP address and Port number of the PLC

SERVER_HOST = "192.168.0.11"      ##put ip address of plc here
SERVER_PORT = 502                ## port no of plc
c = ModbusClient()                              #### Create an instance of the Modbus Client and this will be used further
c.host(SERVER_HOST)             
c.port(SERVER_PORT)       

##### Declaring all the addresses that will be used on PLC side

CX_addr=50             #Coordinates for x axis
SX_addr=14             #Sign for x axis

CY_addr=51             #Coordinates for y axis
SY_addr=15             #Sign for y axis

Colour_addr = 52       #green =1 ; yellow = 2

CTC_addr = 99          #Acknowledgement bit comming at this address will start the process

done_addr = 13         #To inform the PLC about the finished process

################################################################

end = 0                #Used for flag conditions

##### Starting the main operation

print("Attempting to connect to PLC...")

### Checking if the PC and PLC have established connection
if not c.is_open():
    if not c.open():
        print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

### Once the PLC and PC are connected
if c.is_open():
    print("Done Connecting to PLC...")
    while(1):
        ### The acknowledgement bit that would signal to start the process 
        start = c.read_holding_registers(CTC_addr,1)            
        print("start: ",start )
        c.write_single_coil(done_addr, 0)     ### bit to start process at the Robot side    

        if start[0] == 0:
            end = 0
            print("Updating entry value")
        
        ### If the conditions are satisfied 
        while start[0] == 1 and end == 0:
            print("Capturing Image..")

            if end == 0:

                _,white_frame= cap.read()                            ### Reading frames from the camera
                # white_frame = frame[150:350, 200:460]           ### Crop the frame.
               ## white_frame = frame[20:330, 255:550]  
                white_frame = cv2.resize(white_frame,(640,480)) ### resize the camera output window
                white_hsv = cv2.cvtColor(white_frame, cv2.COLOR_BGR2HSV)   ### Convert the normal image to HSV for further operations
                
                ### Declaring the HSV values to detect the base 
                lower_white = np.array([0,0,87])
                upper_white = np.array([179,52,255])
                # lower_white = np.array([10,0,90])
                # upper_white = np.array([179,255,255])

                white_mask = cv2.inRange(white_hsv, lower_white, upper_white)            ### Creates a mask of the Normal Image with the black and white Image and only subtract the base area
                white_res = cv2.bitwise_and(white_frame,white_frame, mask= white_mask)
                
                ### Find the contours of base
                white_contours, white_hierarchy = cv2.findContours(white_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                
                for white_c in white_contours:
                    
                    white_area = cv2.contourArea(white_c)  ### Get area of the contour detected
                    
                    if white_area>50000:          ## Setting the threshold for base area                      
                        cv2.drawContours(white_frame, white_c, -1, (0, 255, 0), 5)  ## Draw contours of base 

                        #### Declaring the HSV values of the color to be sorted using a dictonary that contains the keys:color name and value: hsv value

                        lower = {'yellow': (0,36,161), 'green': (0,64,0),'red':(0,80,0)}
                        upper = {'yellow':  (179,255,255), 'green': (125,255,255),'red':(71,255,255)}
                        colors = {'yellow': (0, 255, 217), 'green': (0, 255,0),'red':(0,0,255)}
                        # lower = {'red':(0,231,54)}
                        # upper = {'red':(24,255,255)}
                        # colors = {'red':(0,0,255)}


                        global contours,hierarchy
                        for key, value in upper.items():
                            ### Iterate over key: color name and value: hsv value of the color in the upper named dictonary
                            
                            mask = cv2.inRange(white_hsv, lower[key], upper[key])

                            ### declaring kernel size for filter to be applied 
                            kernel = np.ones((9, 9), np.uint8)
                            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

                            ### Find the contours of the objects 
                            contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                            for col_cont in contours:
                                
                                col_area = cv2.contourArea(col_cont)         ### Get area of the contour detected
                                c__ = max(contours, key=cv2.contourArea)     ### Sorting the contours with highest area first
                                
                                if col_area > 1200 and col_area < 6500:      ## Setting the threshold for object area
                                    cv2.drawContours(white_frame, col_cont, -1, (0, 0, 255), 2)    ## draw the contour on the image    
                                    ((x, y), radius) = cv2.minEnclosingCircle(c__)     ### Extracting x and y coordinates of the contours of the object

                                    if colors[key] == (0, 0, 255):
                                        ### If the object detected is yellow then 2 is sent to the Robot via PLC
                                          
                                        print ("Detected color is red: ")
                                        c.write_single_register(Colour_addr,2)    
                                    
                                    elif colors[key] == (0,255,0):                     
                                        ### If the object detected is green then 1 is sent to the Robot via PLC
                                      
                                        print ("Detected color is Green: ")
                                        c.write_single_register(Colour_addr,1)     
                                        
                
                ### Converting the object coordinates of the color detected into the coordinates of Robot 

                # dcxx=int(y*(0.6171)-121.31)


                # dcyy=int(x*(-0.4526)+484.14)

                dcxx=int(y*(-0.6989)+769.34)
                dcyy=int(x*(-0.6805)+219.68)
                print(dcxx,dcyy)
                
                """ 
                Check of Negative values
                
                If the value is negative: we cannot transmit a negative value over Modbus 
                so we transform it into a postive value and send a 1 to the address of X and Y (whichever is negative)
                
                """
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
                
                c.write_single_coil(done_addr, 1)  ### ### bit to end process at the Robot side   

                ### Display the frames
                
                cv2.imshow("Res",white_frame)      
                cv2.imshow("Mask",mask)

                print("programm done")
                
                cv2.waitKey(10000) 

                end = 1
                if end == 1:
                    break
            
cv2.destroyAllWindows()