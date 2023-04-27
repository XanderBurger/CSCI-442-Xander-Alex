import pyrealsense2 as rs
import cv2
import numpy as np
from maestro import Controller
from stateMachine import StateMachine

class MiningTango:
    def __init__(self, startingState) -> None:
        self.stateMachine = StateMachine(startingState)
        self.controller = Controller()
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    def process(self, image_frame, depth_frame):
        self.stateMachine.process(self, image_frame, depth_frame)  