### Import all required libraries
import cv2
import numpy as np
import time
from smbus2 import SMBus
                                     
cap = cv2.VideoCapture(0)  ## Initialize the Webcam
'''
0 - for 1st Webcam
2- for 2nd Webcam
'''

width = 640     # set width of the camera window
height = 480     # set height of the camera window       
'''
the width and heigth of the camera window can be changed but it changes the camera co-odinates
'''

detected_color = 0  
'''
detected color indiactes 1 or 2  according to the color recognized 
this can be increased further if required by adding the color HSV values below on line 75 and 76
'''
flag = 0
task_input = int(input("Enter the desired task  1 for color sorting or 2 for pick and place:")) # take user input 
'''
if the user gives task input as 1 then the system woukd initiate color sorting task 
else if the user inputs 2 then it will initiate the shape pick and place task
'''
if task_input == 1:    
    while(cap.isOpened()):

        box_ret, box_frame = cap.read()    ## Read the camera sontents
        if flag % 5 == 0:
            with SMBus(1) as bus:    ### Initialise the i2c communication
                data = [0,169,1,160,0,78,0,1]   ### the data to be transfered is sent in a group to arduino using i2c communication
                bus.write_i2c_block_data(20,0,data) ### this command sends the data to arduino 
                '''
                20 - address of the bus set on the recievers side
                0 - offeset xpected of the value
                data - the list of commands to be sent
                '''
                time.sleep(5)
            box_frame = cv2.resize(box_frame,(width,height)) ### resize the camera output window
            box_frame=cv2.flip(box_frame,-1)   ### As the camera would show mirror images we flip it so that it shows proper images
            box_hsv = cv2.cvtColor(box_frame, cv2.COLOR_BGR2HSV)

            box_lower_blue = np.array([100,92,90])
            box_upper_blue = np.array([149,245,255])
            '''
            box_lower_blue and box_upper_blue are the range of blue colour i.e it will look for the bluw color bin
            '''
            box_mask = cv2.inRange(box_hsv, box_lower_blue, box_upper_blue)
            box_res = cv2.bitwise_and(box_frame,box_frame, mask= box_mask)
            box_contours, box_hierarchy = cv2.findContours(box_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            '''
            finding contours of blue color detected 
            contours - outlines of and object are called contours
            '''
            cv2.line(box_frame,(0,0),(640,0), (0,0,255), 4)
            cv2.line(box_frame,(640,0),(620,10), (0,0,255), 5)
            cv2.putText(box_frame,"x-axis", (70,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),2)
            cv2.line(box_frame,(0,0),(0,480), (0, 255, 0), 4)  
            cv2.line(box_frame,(0,480),(10,460), (0,255,0), 5)
            text=cv2.putText(box_frame,"y-axis", (10,60),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(box_frame,"Origin", (10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.circle(box_frame, (0,0), 8, (0, 0, 0), -1)    
     
            for box_c in box_contours:
                box_area = cv2.contourArea(box_c)  ### Get area of the contour detected
                if box_area>50000:          ## Setting the threshold for blue area
                    print(box_area)                       
                    cv2.drawContours(box_frame, box_c, -1, (0, 255, 0), 5)  ## Draw contours of blues color
                    hsv = cv2.cvtColor(box_frame, cv2.COLOR_BGR2HSV)
                    lower = {'yellow': (20,150,0), 'green': (90, 120, 30)}
                    upper = {'yellow':  (29,255,255), 'green': (109, 245, 255)}
                    colors = {'yellow': (0, 255, 217), 'green': (0, 255,0)}
                    '''
                    lower - lower hsv range of the colour to be detected
                    upper - upper hsv range of the colour to be detected
                    colors - HSV values of the color to be detected
                    '''
                    global contours,hierarchy
                    for key, value in upper.items():
                        
                        mask = cv2.inRange(hsv, lower[key], upper[key])
                        kernel = np.ones((9, 9), np.uint8)
                        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                        contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                        '''
                        Find the contours of the objects kept in the blue bin
                        '''
                        com_X=[]
                        com_Y=[]
                        '''
                        Empty lists created to be accessed further
                        '''
                        for box_c in contours:
                            link_area = cv2.contourArea(box_c) ## find area of the contours of objects detected
                            c = max(contours, key=cv2.contourArea) ### get the contour with the maximum area
                            if link_area>1200 and link_area<6500: ### Setting the upper and lower threshold 
                                
                                cv2.drawContours(box_frame, box_c, -1, (0, 0, 255), 2)    ## draw the contour on the image    
                                ((x, y), radius) = cv2.minEnclosingCircle(c)     

                                M = cv2.moments(c)  ### Get centre of the contours detected
                                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                                if colors[key] == (0, 255, 217):
                                    '''
                                    If the color detected is yellow it will indicate to the arduino so that is 
                                    moves the arm accordingly 
                                    '''
                                    detected_color = 1     
                                    print ("Detected color is yellow: ")
                                elif colors[key] == (0,255,0):
                                    '''
                                    If the color detected is red it will indicate to the arduino so that is 
                                    moves the arm accordingly 
                                    '''
                                    detected_color = 2
                                    print ("Detected color is Green: ")

                                if radius > 0.5:
                                        cv2.circle(box_frame, (int(x), int(y)), int(radius), colors[key], 5)
                                        cv2.putText(box_frame, key + "color", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                                    colors[key], 2)
                                link_M = cv2.moments(box_c)

                                if link_M["m00"] != 0:
                                    global link_cX,link_cY
                                    link_cY = int(link_M["m10"] / link_M["m00"])
                                    link_cX = int(link_M["m01"] / link_M["m00"])
                            
                                if link_cX!=0 and link_cY!=0:
                                    cv2.circle(box_frame, (link_cY, link_cX), 2, (0, 0, 255), -1)
                                    cv2.putText(box_frame, str(link_cX)+ "," + str(link_cY), (link_cY -5 , link_cX -5 ),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                                    cv2.imshow('Link_frame',box_frame)
                                    cv2.imshow('Link_mask',box_mask)
                                
                                    com_X.append(link_cX) 
                                    com_Y.append(link_cY)
                                    '''
                                    Put the values of the x and y coordintes of the detected into the lists created
                                    '''
                                    cv2.waitKey(1000)                                

                            elif box_area>100000:
                                pass
                            else:
                                print("No link detected")
                        print("The X co-ordinates system list is: " + str(com_X)) 
                        print("The Y co-ordinates system list is: " + str(com_Y)) 
                        print("Hence the Number of links : " + str(len(com_X)))

                        if(len(com_X)>=1):
                            with SMBus(1) as bus:

                                '''
                                Insert Calculated values here for calibration
                                '''   
                                dcxx=int(com_X[0]*(-0.41)+96.01)
                                dcyy=int(com_Y[0]*(-0.58)-41.81)
                                command = 1
                                '''
                                The formula to match the camera and Dobot coordinate system 
                                the formula is derived using the Euclidean distance and the slope formula 
                                from Coordinate geometry
                                '''
                                print("Dobot co-ordinates: " + str(dcxx) + " " + str(dcyy))
                                if dcxx>0:
                                    dcx=0    
                                else:
                                    dcxx=-dcxx
                                    dcx=1

                                if dcyy>0:
                                    dcy=0
                                else:
                                    dcyy=-dcyy
                                    dcy=1

                                '''
                                The values to move the Dobot and pick it from a particular calculated coordinate
                                are sent through i2c communication using SMBus library
                                
                                Sequence:
                                1. dcx - 0/1  0: if the x coordinates are +ve 
                                           1: if the coordinates are -ve  and it will be made -ve on arduino side 
                                           and then fed to Dobot
                                2. dcxx - X coordinates of the object detected 

                                3. dcy - 0/1  0: if the y coordinates are +ve 
                                           1: if the coordinates are -ve  and it will be made -ve on arduino side 
                                           and then fed to Dobot
                                4. dcyy - Y coordinates of the object detected

                                5. dcz - 0/1  0: if the z coordinates are +ve 
                                           1: if the coordinates are -ve  and it will be made -ve on arduino side 
                                           and then fed to Dobot
                                6. dczz - Z coordinates of the object detected
                                7. 0/1 - 0: suction cup deactivated
                                         1: suction activated
                                8.  1- to move the slider 
                                9. detected color: indiacted the arduino to move any 1 of the two diverter arm to move
                                                   according to the color detected 
                                                   
                                                   yellow - 1st arm moves
                                                   red - 2nd arm moves
                                '''
                                data = [0,160,1,173,0,122,0,1,detected_color]       
                                bus.write_i2c_block_data(20,0,data)
                                time.sleep(3)

                                data = [dcx,dcxx,dcy,dcyy,0,100,0,1]
                                bus.write_i2c_block_data(20,0,data)
                                time.sleep(3)
                                
                                data = [dcx,dcxx,dcy,dcyy,1,72,1,1,detected_color]
                                bus.write_i2c_block_data(20,0,data)
                                time.sleep(3)
                                
                                data = [dcx,dcxx,dcy,dcyy,0,100,1,1,detected_color]
                                bus.write_i2c_block_data(20,0,data)
                                time.sleep(3)
                                
                                data = [0,169,1,160,0,78,1,1,detected_color]    
                                bus.write_i2c_block_data(20,0,data)
                                time.sleep(3)
                                
                                data = [0,169,1,160,0,78,1,5,detected_color]    
                                bus.write_i2c_block_data(20,0,data)
                                time.sleep(3)
                                
                                time.sleep(20)           

                                break
                        
                    else:
                        print("No bin detected") 

        
        if flag==100:
            flag=0
        flag = 1+flag     

        cv2.imshow("Frame",box_frame) ### show the camera Image
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        print(flag)
    
    '''
if when asked the user inputs 2 the arduino will carry out shape pick and place task
'''    
elif task_input == 2: 
    with SMBus(1) as bus: 
                data = [0,169,1,160,0,78,0,1,55]         
                bus.write_i2c_block_data(20,0,data)
                time.sleep(10)
                data = [0,169,1,160,0,78,0,1,100]         
                bus.write_i2c_block_data(20,0,data)
                time.sleep(5)
    print("Values sent")