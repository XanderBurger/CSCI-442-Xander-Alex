from stateMachine.state import State
import cv2
import numpy as np

class FindMiningArea(State):
    
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        pass

    def process(self, tango, color_frame, depth_frame):
        nextState = None
        corners, ids, rejected = cv2.aruco.detectMarkers(color_frame, self.arucoDict)
        depthToMine = None

        try:
            for i in range(len(ids)):
                if int(ids[i]) == 22:
                    print("found mine")
                    box = corners[i][0]
                    centerX = int((box[0][0] + box[1][0]) / 2)
                    centerY = int((box[1][1] + box[3][1]) / 2)
                    depthToMine = depth_frame.get_distance(centerX, centerY)
                    
                    if depthToMine == 0:
                        self.forwardSpeed = 6000
                        continue

                    if centerX >= 400:
                        print("Turn Right")
                        self.turnSpeed = 5400
                    elif centerX <= 200:
                        print("Turn Left")
                        self.turnSpeed = 6500
                    elif centerX < 400 and centerX > 200:
                        if depthToMine < 1.5:
                            self.forwardSpeed = 5100
                        else:
                            self.forwardSpeed = 6000
                            print("found Mine")
                            nextState = "MINING AREA"
                    
                    print("Depth to marker ->", depthToMine)
                    cv2.aruco.drawDetectedMarkers(color_frame, corners)

                else:
                    self.turnSpeed = 5310
                    self.forwardSpeed = 6000
                    print("not mining area")
        
        except TypeError:
            self.turnSpeed = 5310
            self.forwardSpeed = 6000
            print("NO MARKER FOUND")

        tango.controller.setTarget(self.TURN, self.turnSpeed)
        tango.controller.setTarget(self.FORWARD, self.forwardSpeed)

        return nextState
    
    def exitState(self, tango):
        pass