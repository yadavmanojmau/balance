import cv2
import numpy
width = 640
height = 480
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(cap, str(x) + ',' +
                    str(y), (x, y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', cap)

    if event == cv2.EVENT_RBUTTONDOWN:

        print(x, ' ', y)

        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(cap, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x, y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', cap)

camera = cv2.VideoCapture(0)
# camera.set(3,480)
# camera.set(4,640)
width = 640     # set width of the camera window
height = 480 
while True:
    _,cap = camera.read()
    cap = cv2.resize(cap,(width,height))
    cap=cv2.flip(cap,-1)
    cv2.line(cap,(0,0),(640,0), (0,0,255), 4)
    cv2.line(cap,(640,0),(620,10), (0,0,255), 5)
    cv2.putText(cap,"x-axis", (70,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),2)
    cv2.line(cap,(0,0),(0,480), (0, 255, 0), 4)  
    cv2.line(cap,(0,480),(10,460), (0,255,0), 5)
    text=cv2.putText(cap,"y-axis", (10,60),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.putText(cap,"Origin", (10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.imshow('image', cap)
    cv2.setMouseCallback('image', click_event)
    if cv2.waitKey(1) == ord('q'):
        break