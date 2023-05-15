#### Import necessary libraries ####
import cv2                                        ####  Computer Vision Library
import numpy as np                                  
from smbus2 import SMBus
import time
import smbus2
""" 
Capture Frame from the Webcam
                                                                  c.write_single_register(52,2)    

1: for 2nd camera
and continue if any more connected
"""
cap = cv2.VideoCapture(0)

detected_color = 0  
### Declare the IP address and Port number of the PLC


end = 0                #Used for flag conditions

while(1):


        
   # print("Capturing Image..")

     if end == 0:

                _,frame = cap.read()                            ### Reading frames from the camera
                white_frame = frame[150:350, 200:460]           ### Crop the frame.
                white_frame = cv2.resize(white_frame,(640,480)) ### resize the camera output window
                white_hsv = cv2.cvtColor(white_frame, cv2.COLOR_BGR2HSV)   ### Convert the normal image to HSV for further operations
                
                ### Declaring the HSV values to detect the base 
                lower_white = np.array([0,0,87])
                upper_white = np.array([179,52,255])
                
                white_mask = cv2.inRange(white_hsv, lower_white, upper_white)            ### Creates a mask of the Normal Image with the black and white Image and only subtract the base area
                white_res = cv2.bitwise_and(white_frame,white_frame, mask= white_mask)
                
                ### Find the contours of base
                white_contours, white_hierarchy = cv2.findContours(white_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                
                for white_c in white_contours:
                    
                    white_area = cv2.contourArea(white_c)  ### Get area of the contour detected
                    
                    if white_area>50000:          ## Setting the threshold for base area                      
                        cv2.drawContours(white_frame, white_c, -1, (0, 255, 0), 5)  ## Draw contours of base 

                        #### Declaring the HSV values of the color to be sorted using a dictonary that contains the keys:color name and value: hsv value

                        lower = {'yellow': (4,90,0), 'green': (66,66,76),'red':(0,142,158)}
                        upper = {'yellow':  (67,255,255), 'green': (154,255,255),'red':(9,255,221)}
                        colors = {'yellow': (0, 255, 217), 'green': (0, 255,0),'red':(0,0,255)}

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

                                    if colors[key] == (0, 255, 217):
                                     
                                        print ("Detected color is yellow: ")
                                        detected_color = 1  
                                    
                                    elif colors[key] == (0,255,0):                     
                                     
                                        print ("Detected color is Green: ")
                                        detected_color = 2 
                                    else:
                                        print("no bin detect")
                                         
     
                                with SMBus(1) as bus:
                                 
                                    dcxx=int(y*(0.4079)+153.96)
                                    dcyy=int(x*(-0.9853)+178.78)
                                    print(dcxx,dcyy)
                                    command = 1
                                    # print("Dobot co-ordinates: " + str(dcxx) + " " + str(dcyy))
                
                                    """ 
                                    Check of Negative values
                                    
                                    If the value is negative: we cannot transmit a negative value over Modbus 
                                    so we transform it into a postive value and send a 1 to the address of X and Y (whichever is negative)
                                    
                                    """
                                
                                    if dcxx > 0:
                                        dcx=0
                                    else:
                                        dcxx=-dcxx
                                        dcx=1
                                        
                                    if dcyy >0:
                                        dcy =0
                                    else:
                                        dcyy=-dcyy
                                        dcy=1

                                

                                    data = [0,200,0,9,0,78,1,1,detected_color]    
                                    bus.write_i2c_block_data(20,0,data)
                                    time.sleep(3)
                                
                                    data = [dcx,dcxx,dcy,dcyy,1,100,0,5,detected_color]    
                                    bus.write_i2c_block_data(20,0,data)
                                    time.sleep(3)
                                
                                   # time.sleep(20)  
                                    cv2.waitKey(100) 

                                    break

                               
                                      
                
                
                cv2.imshow("Res",white_frame)      
                cv2.imshow("Mask",mask)
                cv2.waitKey(10) 

                end = 0
                if end == 1:
                 break
            
cv2.destroyAllWindows()