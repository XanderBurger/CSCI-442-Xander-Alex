import cv2
import numpy as np

class State:
    def __init__(self) -> None:
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.FORWARD = 0
        self.TURN = 1
        self.HEADTILT = 4
        self.forwardSpeed = 6000
        self.turnSpeed = 6000

    
    def enterState(self, tango):
        pass

    def process(self, tango, color_frame, depth_frame):
        pass
    
    def exitState(self, tango):
        pass