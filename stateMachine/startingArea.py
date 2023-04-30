from stateMachine.state import State
import cv2
import numpy as np
import time

class StartingArea(State):
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        time.sleep(1.7)
        tango.controller.setTarget(self.FORWARD, 6000)
        tango.controller.setTarget(self.HEADTILT, 5000)
        print("IN START")


    def process(self, tango, color_frame, depth_frame):
        nextState = None
        hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

        yellowBinary = cv2.inRange(hsv_frame, tango.yellowLower, tango.yellowUpper)
        greenBinary = cv2.inRange(hsv_frame, tango.greenLower, tango.greenUpper)
        pinkBinary = cv2.inRange(hsv_frame, tango.pinkLower, tango.pinkUpper)
        orangeBinary = cv2.inRange(hsv_frame, tango.orangeLower, tango.orangeUpper)
        blueBinary = cv2.inRange(hsv_frame, tango.blueLower, tango.blueUpper)

        yellowContours, yellowHierarchy = cv2.findContours(yellowBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        greenContours, greenHierarchy = cv2.findContours(greenBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        pinkContours, pinkHierarchy = cv2.findContours(pinkBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        orangeContours, orangeHierarchy = cv2.findContours(orangeBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        blueContours, blueHierarchy = cv2.findContours(blueBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(color_frame, yellowContours, -1, (255,255,0), 2)
        cv2.drawContours(color_frame, greenContours, -1, (0,255,0), 2)
        cv2.drawContours(color_frame, pinkContours, -1, (50, 0 ,255), 2)
        cv2.drawContours(color_frame, orangeContours, -1, (255, 0 ,255), 2)
        cv2.drawContours(color_frame, blueContours, -1, (255, 0 , 0), 2)

        if len(yellowContours) > 0:
            ycMax = max(yellowContours, key=cv2.contourArea)
            M = cv2.moments(ycMax)
            if M["m00"] != 0:
                ycX = int(M["m10"] / M["m00"])
                ycY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (ycX, ycY), 5, (255,255,0), 2)
        
        if len(greenContours) > 0:
            gcMax = max(greenContours, key=cv2.contourArea)
            M = cv2.moments(gcMax)
            if M["m00"] != 0:
                gcX = int(M["m10"] / M["m00"])
                gcY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (gcX,gcY), 5, (255,255,0), 2)

        if len(pinkContours) > 0:
            pcMax = max(pinkContours, key=cv2.contourArea)
            M = cv2.moments(pcMax)
            if M["m00"] != 0:
                pcX = int(M["m10"] / M["m00"])
                pcY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (pcX, pcY), 5, (255,255,0), 2)
            
        if len(orangeContours) > 0:
            ocMax = max(orangeContours, key=cv2.contourArea)
            M = cv2.moments(ocMax)
            if M["m00"] != 0:
                ocX = int(M["m10"] / M["m00"])
                ocY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (ocX, ocY), 5, (255,255,0), 2)
    
        if len(blueContours) > 0:
            bcMax = max(blueContours, key=cv2.contourArea)
            M = cv2.moments(bcMax)
            if M["m00"] != 0:
                bcX = int(M["m10"] / M["m00"])
                bcY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (bcX, bcY), 5, (255,255,0), 2)
        
        nextState = "FIND MINE"
        return nextState

    
    def exitState(self, tango):
        pass