import cv2

cap = cv2.VideoCapture(0)

while True:
    _,frame = cap.read()
    frame_ = frame[150:420, 100:520]
    white_frame = cv2.resize(frame_,(640,480))
    cv2.imshow("res",frame)
    cv2.imshow("resss",white_frame)
    cv2.waitKey(1)
    
cv2.destroyAllWindows()
