import cv2                                        ####  Computer Vision Library
import numpy as np                                  
from pyModbusTCP.client import ModbusClient       ####  for establishing Communication between PLC and PC
import time
from numpy.core.fromnumeric import shape
from shape_class import ShapeDetector

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)

### Declare the IP address and Port number of the PLC

# SERVER_HOST = "192.168.0.10"
# SERVER_PORT = 502
# c = ModbusClient()                              #### Create an instance of the Modbus Client and this will be used further
# c.host(SERVER_HOST)
# c.port(SERVER_PORT)
c1 = ModbusClient(host="192.168.0.12",port=502,unit_id=1, auto_open=True)  # Create an instance of the Modbus Client and this will be used further
##### Declaring all the addresses that will be used on PLC side

CX_addr=50             #Coordinates for x axis
SX_addr=14             #Sign for x axis

CY_addr=51             #Coordinates for y axis
SY_addr=15             #Sign for y axis

Shape_addr = 52       #square =1 ; triangle = 2

CTC_addr = 99          #Acknowledgement bit comming at this address will start the process

done_addr = 13         #To inform the PLC about the finished process

################################################################

end = 0                #Used for flag conditions

sd = ShapeDetector()

print("Attempting to connect to PLC...")

### Checking if the PC and PLC have established connection
# if not c.is_open():
#     if not c.open():
#         print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

# ### Once the PLC and PC are connected
# if c.is_open():
#     print("Done Connecting to PLC...")
while(1):
        ### The acknowledgement bit that would signal to start the process 
        start = c1.read_holding_registers(CTC_addr,1)            
        print("start: ",start )
        c1.write_single_coil(done_addr, 0)     ### bit to start process at the Robot side    

        if start[0] == 0:
            end = 0
            print("Updating entry value")
        
        ### If the conditions are satisfied 
        while start[0] == 1 and end == 0:
            print("Capturing Image..")

            if end == 0:

                success, img= cap.read()         ### Reading frames from the camera
                ##img = img_[150:420, 100:520]       ### Crop the frame.
                img = cv2.resize(img,(frameWidth,frameHeight)) ### resize the camera output window
                
                imgBlur = cv2.GaussianBlur(img, (7, 7), 1)     ### Applying Gaussian Blur to the frame
                imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)   ### Gray scaling the frame
                imgCanny = cv2.Canny(imgGray,91,156)  ### Extracting only edges of the objects
                imgCanny = cv2.Canny(imgGray,47,9)  ### Extracting only edges of the objects
                kernel = np.ones((5, 5))
                imgDil = cv2.dilate(imgCanny, kernel, iterations=1) ### Dilation: Removing the excess noise from the Image
                
                ### Find the contours of shapes
                contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                for cnt in contours:
                    area = cv2.contourArea(cnt)    ### Get area of the contour detected
                    c_ = max(contours, key=cv2.contourArea)

                    if    1000 < area < 11500:        ## Setting the threshold for base area

                        cv2.drawContours(img, cnt, -1, (255, 0, 255), 3)   ## Draw contours of base
                        ((x_, y_), radius) = cv2.minEnclosingCircle(c_)    ### Extracting x and y coordinates of the contours of the shapes
  
                        cv2.circle(img, (int(x_), int(y_)), int(radius), (0,255,0), 2)   ### Draw a circle around the detected shape
                        
                        ### Creating a variable instance of the shapedetector Class that would return us the shape detected
                        shape = sd.shape_detector(c_)           

                        ### If the detected shape is circle send the command to the robot to move accordingly
                        if shape == 'Circle':
                            cv2.putText(img,"Shape: " + str("Circle"), (50,50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255,0), 2)
                            print("Detected circle: ")
                            c1.write_single_register(Shape_addr,1)
                        
                        ### If the detected shape is Square send the command to the robot to move accordingly
                        if shape == 'Square':
                            cv2.putText(img,"Shape: " + str("Square"), (50,50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255,0), 2)
                            print("Detected square ")
                            c1.write_single_register(Shape_addr,2)
                        

                ### Converting the object coordinates of the shapes detected into the coordinates of Robot 
                # dcxx=int(y_*(-0.7025)+767.54)
                # dcyy=int(x_*(-0.6743)+216.75)
                # print("dcxx:",dcxx,"dcyy:",dcyy)
                dcxx=int(y_*(-0.6074)+753.68)
                dcyy=int(x_*(-0.608)+299.37)
                print(dcxx,dcyy)
                
                """ 
                Check of Negative values
                
                If the value is negative: we cannot transmit a negative value over Modbus 
                so we transform it into a postive value and send a 1 to the address of X and Y (whichever is negative)
                
                """

                cv2.putText(img, "X coordinates: " + str(dcxx), (400,50), cv2.FONT_HERSHEY_COMPLEX, .5,
                                  (0,0,0), 1)
                cv2.putText(img, "Y coordinates: " + str(dcyy), (400,100), cv2.FONT_HERSHEY_COMPLEX, .5,
                                    (0,0,0), 1)

                if dcxx < 0:
                    dcxx = (dcxx * (-1))
                    c1.write_single_coil(SX_addr,1)
                else:
                    c1.write_single_coil(SX_addr,0)
                if dcyy < 0:
                    dcyy = (dcyy * (-1))
                    c1.write_single_coil(SY_addr,1)
                else:
                    c1.write_single_coil(SY_addr,0)

                P_CX = c1.write_single_register(CX_addr, int(dcxx))
                P_CY = c1.write_single_register(CY_addr, int(dcyy))
                
                c1.write_single_coil(done_addr, 1)  ### ### bit to end process at the Robot side   

                ### Display the frames

                cv2.imshow("IMG", img)
                cv2.imshow("Canny",imgCanny)
                cv2.imshow("Dilute",imgDil)
                
                cv2.waitKey(10000)

                end = 1
                if end == 1:
                    break
cap.release()               
cv2.destroyAllWindows()
