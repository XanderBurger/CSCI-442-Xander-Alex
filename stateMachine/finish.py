from stateMachine.state import State
import cv2
import numpy as np
import time

class Finish(State):
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        print("FINISHED!!!!")

    def process(self, tango, color_frame, depth_frame):
        nextState = None
        return nextState
    
    def exitState(self, tango):
        pass