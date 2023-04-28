from stateMachine.state import State
import cv2
import numpy as np


class MiningState(State):
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        pass

    def process(self, tango, color_frame, depth_frame):
        print("mining state")
    
    def exitState(self, tango):
        pass