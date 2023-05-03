from stateMachine.state import State
import cv2
import numpy as np
import time

class Test(State):
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        print("test")

    def process(self, tango, color_frame, depth_frame):
        nextState = None

        hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

        yellowBinary = cv2.inRange(hsv_frame, tango.yellowLower, tango.yellowUpper)
        greenBinary = cv2.inRange(hsv_frame, tango.greenLower, tango.greenUpper)
        pinkBinary = cv2.inRange(hsv_frame, tango.pinkLower, tango.pinkUpper)
        blueBinary = cv2.inRange(hsv_frame, tango.blueLower, tango.blueUpper)
        orangeBinary = cv2.inRange(hsv_frame, tango.orangeLower, tango.orangeUpper)
        
        orangeContours, orangeHierarchy = cv2.findContours(orangeBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        blueContours, blueHierarchy = cv2.findContours(blueBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        yellowContours, yellowHierarchy = cv2.findContours(yellowBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        greenContours, greenHierarchy = cv2.findContours(greenBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        pinkContours, pinkHierarchy = cv2.findContours(pinkBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.drawContours(color_frame, orangeContours, -1, (255, 0 ,255), 2)
        cv2.drawContours(color_frame, blueContours, -1, (255, 0 ,255), 2)
        cv2.drawContours(color_frame, yellowContours, -1, (255,255,0), 2)
        cv2.drawContours(color_frame, greenContours, -1, (0,255,0), 2)
        cv2.drawContours(color_frame, pinkContours, -1, (50, 0 ,255), 2)

        return nextState
    
    def exitState(self, tango):
        pass