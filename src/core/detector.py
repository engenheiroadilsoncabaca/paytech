import cv2
import numpy as np

class SupplyEventDetector:
    def __init__(self, roi_coords=None):
        
        self.roi_coords = roi_coords
        
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, 
            varThreshold=50, 
            detectShadows=True
        )

    def detect_motion_in_roi(self, frame):
    
        if self.roi_coords:
            y1, y2, x1, x2 = self.roi_coords
            roi = frame[y1:y2, x1:x2]
        else:
            roi = frame

        #Pré-processamento
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        blur_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
        
        fg_mask = self.background_subtractor.apply(blur_roi)

        _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        pixel_count = np.sum(thresh == 255)
        
        limiar_de_movimento = 1500 
        
        return pixel_count > limiar_de_movimento