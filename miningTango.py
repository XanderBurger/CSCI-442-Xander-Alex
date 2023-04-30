import pyrealsense2 as rs
import cv2
import numpy as np
from maestro import Controller
from stateMachine import stateMachine

class MiningTango:
    def __init__(self, startingState) -> None:
        self.stateMachine = stateMachine.StateMachine(self, startingState)
        self.controller = Controller()
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

        self.iceBlockColor = None
        self.face_cascade = cv2.CascadeClassifier("data/haarcascades/haarcascade_frontalface.xml")
        
        self.yellowUpper = np.array([40,240,255])
        self.yellowLower = np.array([30,170,150])

        self.greenUpper = np.array([67,160,255])
        self.greenLower = np.array([55,120,170])

        self.pinkUpper = np.array([175,230,255])
        self.pinkLower = np.array([160,130,170])

        self.orangeUpper = np.array([20,220,255])
        self.orangeLower = np.array([10,130,200])

        self.blueUpper = np.array([100,255,255])
        self.blueLower = np.array([85,200,140])
        

    def process(self, image_frame, depth_frame):
        self.stateMachine.process(self, image_frame, depth_frame)