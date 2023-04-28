from stateMachine import state
import cv2
import numpy as np


class MiningArea(state.State):
    def __init__(self) -> None:
        pass

    def enterState(self, tango):
        pass

    def process(self, tango, color_frame, depth_frame):
        print("mining state")
    
    def exitState(self, tango):
        pass