import cv2

class ShapeDetector:
    
    def __init__(self):
        pass
     
    def shape_detector(self,contour):
        
        shape = "unidentified"
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        if len(approx) == 3:
            shape = "Triangle"

        elif len(approx) == 4:
            shape = "Square"
        
        elif len(approx) == 6:
            shape = "Hexagoan"
        
        else:       
            shape = "Circle"

        return shape
