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
        
        self.yellowUpper = np.array([40,240,200])
        self.yellowLower = np.array([30,180,150])
        self.greenUpper = np.array([65,200,220])
        self.greenLower = np.array([55,140,180])
        self.pinkUpper = np.array([175,200,255])
        self.pinkLower = np.array([160,140,190])
        self.orangeUpper = np.array([20,220,255])
        self.orangeLower = np.array([10,130,200])
        self.blueUpper = np.array([95,240,240])
        self.blueLower = np.array([80,100,200])
        

    def process(self, image_frame, depth_frame):
        self.stateMachine.process(self, image_frame, depth_frame)