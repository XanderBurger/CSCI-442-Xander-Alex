from stateMachine.state import State
import cv2
import numpy as np

class FindStartingArea(State):
    
    def __init__(self) -> None:
        super().__init__()


    def enterState(self, tango):
        tango.controller.setTarget(self.FORWARD, 6000)
        tango.controller.setTarget(self.HEADTILT, 5000)
    
    def process(self, tango, color_frame, depth_frame):
        nextState = None
        corners, ids, rejected = cv2.aruco.detectMarkers(color_frame, self.arucoDict)
        self.turnSpeed = 5150

        try:
            for i in range(len(ids)):
                if int(ids[i]) == 22:
                    print("found mine")
                    box = corners[i][0]
                    centerX = int((box[0][0] + box[1][0]) / 2)
                    centerY = int((box[1][1] + box[3][1]) / 2)

                    if centerX >= 350:
                        self.turnSpeed = 5050
                    elif centerX <= 250:
                        self.turnSpeed = 6950
                    elif centerX < 350 and centerX > 250:
                        self.turnSpeed = 6000
                        nextState = "GO TO START"
                        
                    cv2.circle(color_frame, (centerX, centerY), 5, (255, 255, 0), 2)
                    cv2.aruco.drawDetectedMarkers(color_frame, corners)
                else:
                    self.turnSpeed = 5050
        except TypeError:
            self.turnSpeed = 5100
            self.forwardSpeed = 6000
            print("NO MARKER FOUND")
        
        tango.controller.setTarget(self.TURN, self.turnSpeed)
        tango.controller.setTarget(self.FORWARD, self.forwardSpeed)
        
        return nextState
    
    def exitState(self, tango):
        pass