from stateMachine.state import State
import cv2
import numpy as np
import time

class GoToStart(State):
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        tango.controller.setTarget(self.TURN, 6000)
        tango.controller.setTarget(self.HEADTILT, 4000)
        print("GOING TO START")

    def process(self, tango, color_frame, depth_frame):
        nextState = None
        hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

        orangeBinary = cv2.inRange(hsv_frame, tango.orangeLower, tango.orangeUpper)
        orangeContours, orangeHierarchy = cv2.findContours(orangeBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(color_frame, orangeContours, -1, (255, 0 ,255), 2)
        self.forwardSpeed = 5100  
        if len(orangeContours) > 0:
            ocMax = max(orangeContours, key=cv2.contourArea)
            M = cv2.moments(ocMax)
            if M["m00"] != 0:
                ocX = int(M["m10"] / M["m00"])
                ocY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (ocX, ocY), 5, (255,255,0), 2)

                if ocY > 465:
                    return "STARTING AREA"
        
        
        tango.controller.setTarget(self.FORWARD, self.forwardSpeed)

        return nextState
    
    def exitState(self, tango):
        time.sleep(1.7)
        tango.controller.setTarget(self.FORWARD, 6000)
        tango.controller.setTarget(self.HEADTILT, 5000)