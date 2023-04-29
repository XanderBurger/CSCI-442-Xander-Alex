import cv2
import numpy as np

class State:
    def __init__(self) -> None:
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.FORWARD = 0
        self.TURN = 1
        self.forwardSpeed = 6000
        self.turnSpeed = 6000

        self.yellowUpper = np.array([61,92,96])
        self.yellowLower = np.array([57,75,82])
        self.greenUpper = np.array([89,87,94])
        self.greenLower = np.array([86,69,78])
        self.pinkUpper = np.array([322,90,96])
        self.pinkLower = np.array([337,64,79])


    def enterState(self, tango):
        pass

    def process(self, tango, color_frame, depth_frame):
        pass
    
    def exitState(self, tango):
        pass