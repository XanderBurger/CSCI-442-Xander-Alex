import pyrealsense2 as rs
import cv2
import numpy as np
from maestro import Controller
from stateMachine import stateMachine
import time

class MiningTango:
    def __init__(self, startingState) -> None:
        self.stateMachine = stateMachine.StateMachine(self, startingState)
        self.controller = Controller()
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

        self.totalFrames = 0

        self.iceBlockColor = None
        self.face_cascade = cv2.CascadeClassifier("data/haarcascades/haarcascade_frontalface_default.xml")
        
        self.yellowUpper = np.array([40,240,255])
        self.yellowLower = np.array([30,100,140])

        self.greenUpper = np.array([75,255,255])
        self.greenLower = np.array([50,60,170])

        self.pinkUpper = np.array([175,230,255])
        self.pinkLower = np.array([160,130,170])

        self.orangeUpper = np.array([29,220,255])
        self.orangeLower = np.array([20,50,200])

        self.blueUpper = np.array([95,240,240])
        self.blueLower = np.array([85,170,135])
    

    def process(self, image_frame, depth_frame):
        self.stateMachine.process(self, image_frame, depth_frame)
