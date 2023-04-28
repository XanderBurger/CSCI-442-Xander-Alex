from stateMachine.state import State
import cv2
import numpy as np

class FindMiningArea(State):
    
    def __init__(self) -> None:
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.forwardSpeed = 6000
        self.turnSpeed = 6000

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

                    if centerX >= 350:
                        print("Turn Right")
                        self.turnSpeed = 5100
                    elif centerX <= 250:
                        print("Turn Left")
                        self.turnSpeed = 6900
                    elif centerX < 350 and centerX > 250:
                        if depthToMine < 1.5:
                            self.forwardSpeed = 5100
                    
                    print("Depth to marker ->", depthToMine)
                    cv2.aruco.drawDetectedMarkers(color_frame, corners)

                else:
                    self.turnSpeed = 5050
                    self.forwardSpeed = 6000
                    print("not mining area")
                    
        except:
            self.turnSpeed = 5050
            self.forwardSpeed = 6000
            print("NO MARKER FOUND")

        tango.controller.setTarget(1, self.turnSpeed)
        tango.controller.setTarget(0, self.forwardSpeed)

        return nextState