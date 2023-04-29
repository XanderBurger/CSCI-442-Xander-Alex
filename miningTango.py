import pyrealsense2 as rs
import cv2
import numpy as np
from maestro import Controller
from stateMachine import stateMachine

class MiningTango:
    def __init__(self, startingState) -> None:
        self.stateMachine = stateMachine.StateMachine(startingState)
        self.controller = Controller()
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        
        self.yellowUpper = np.array([61,47,93])
        self.yellowLower = np.array([62,54,84])
        self.greenUpper = np.array([92,62,84])
        self.greenLower = np.array([91,71,79])
        self.pinkUpper = np.array([348,67,96])
        self.pinkLower = np.array([342,71,81])
        self.orangeUpper = np.array([33,64,99])
        self.orangeLower = np.array([27,82,82])
        self.blueUpper = np.array([87,39,253])
        self.blueLower = np.array([97,247,198])
        

    def process(self, image_frame, depth_frame):
        self.stateMachine.process(self, image_frame, depth_frame)