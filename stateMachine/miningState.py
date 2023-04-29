from stateMachine.state import State
import cv2
import numpy as np



class MiningState(State):
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        pass

    def process(self, tango, color_frame, depth_frame):
        hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)
        yellowBinary = cv2.inRange(hsv_frame, self.yellowLower, self.yellowUpper)
        greenBinary = cv2.inRange(hsv_frame, self.greenLower, self.greenUpper)
        pinkBinary = cv2.inRange(hsv_frame, self.pinkLower, self.pinkUpper)

        yellowContours, yellowHierarchy = cv2.findContours(yellowBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        greenContours, greenHierarchy = cv2.findContours(greenBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        pinkContours, pinkHierarchy = cv2.findContours(pinkBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(color_frame, yellowContours, -1, (255,255,0), 2)
        cv2.drawContours(color_frame, greenContours, -1, (0,255,0), 2)
        cv2.drawContours(color_frame, pinkContours, -1, (50, 0 ,255), 2)

        for contours in yellowContours:
            M = cv2.moments(contours)
            if M["m00"] == 0:
                continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(color_frame, (cX, cY), 7, (255, 255, 255), 1)
        
        for contours in greenContours:
            M = cv2.moments(contours)
            if M["m00"] == 0:
                continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(color_frame, (cX, cY), 7, (255, 255, 255), 1)

        for contours in pinkContours:
            M = cv2.moments(contours)
            if M["m00"] == 0:
                continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(color_frame, (cX, cY), 7, (255, 255, 255), 1)
    
    
    def exitState(self, tango):
        pass