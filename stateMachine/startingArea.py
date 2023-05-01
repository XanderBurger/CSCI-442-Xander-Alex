from stateMachine.state import State
import cv2
import numpy as np
import time

class StartingArea(State):
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        print("IN START")

    def process(self, tango, color_frame, depth_frame):
        nextState = None
        hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

        colorContours = None
        
        if tango.iceBlockColor == "YELLOW":
            yellowBinary = cv2.inRange(hsv_frame, tango.yellowLower, tango.yellowUpper)
            colorContours, colorContours = cv2.findContours(yellowBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        elif tango.iceBlockColor == "PINK":
            pinkBinary = cv2.inRange(hsv_frame, tango.pinkLower, tango.pinkUpper)
            colorContours, colorContours = cv2.findContours(pinkBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        elif tango.iceBlockColor == "GREEN":
            greenBinary = cv2.inRange(hsv_frame, tango.greenLower, tango.greenUpper)
            colorContours, colorContours = cv2.findContours(greenBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            print("NO ICE BLOCK COLOR")

        cv2.drawContours(color_frame, colorContours, -1, (255,255,0), 2)

        if len(colorContours) > 0:
            cMax = max(colorContours, key=cv2.contourArea)
            M = cv2.moments(cMax)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (cX, cY), 5, (255,255,0), 2)


        return nextState

    
    def exitState(self, tango):
        pass