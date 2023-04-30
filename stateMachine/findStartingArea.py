from stateMachine.state import State
import cv2
import numpy as np

class FindStartingArea(State):
    
    def __init__(self) -> None:
        super().__init__()


    def enterState(self, tango):
        pass
    
    def process(self, tango, color_frame, depth_frame):
        nextState = None
        corners, ids, rejected = cv2.aruco.detectMarkers(color_frame, self.arucoDict)
        # depthToMine = None
    
        try:
            for i in range(len(ids)):
                if int(ids[i]) == 49:
                    print("found mine")
                    box = corners[i][0]
                    centerX = int((box[0][0] + box[1][0]) / 2)
                    centerY = int((box[1][1] + box[3][1]) / 2)
                    # depthToMine = depth_frame.get_distance(centerX, centerY)
                    
                    # if depthToMine == 0:
                    #     self.forwardSpeed = 6000
                    #     self.turnSpeed = 6000
                    #     continue

                    if centerX >= 350:
                        self.turnSpeed = 5050
                    elif centerX <= 250:
                        self.turnSpeed = 6950
                    elif centerX < 350 and centerX > 250:
                        self.turnSpeed = 6000
                        nextState = "GO TO START"
                        # if depthToMine > 1:
                        #     self.forwardSpeed = 4900
                        #     self.turnSpeed = 6000
                        # else:
                        #     self.forwardSpeed = 6000
                        #     self.turnSpeed = 6000
                        #     print("found Mine")
                        #     nextState = "MINING AREA"

                    
                    # print("Depth to marker ->", depthToMine)
                    cv2.circle(color_frame, (centerX, centerY), 5, (255, 255, 0), 2)
                    cv2.aruco.drawDetectedMarkers(color_frame, corners)

        except TypeError:
            self.turnSpeed = 5100
            self.forwardSpeed = 6000
            print("NO MARKER FOUND")
        
        tango.controller.setTarget(self.TURN, self.turnSpeed)
        tango.controller.setTarget(self.FORWARD, self.forwardSpeed)
        
        return nextState
    
    def exitState(self, tango):
        pass