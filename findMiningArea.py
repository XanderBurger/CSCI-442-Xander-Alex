from state import State
import cv2
import numpy as np

class FindMiningArea(State):
    
    def __init__(self) -> None:
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    def enterState(self, tango):
        pass

    def process(self, tango, color_frame, depth_frame):
        nextState = None
        corners, ids, rejected = cv2.aruco.detectMarkers(color_frame, self.arucoDict)
        
        depthToMine = None

        try:
            turnSpeed = 6000
            for i in range(len):
                id = int(ids[i])
                if ids[i] == 22:
                    print("found mine")
                    box = corners[i][0]
                    centerX = int((box[0][0] + box[1][0]) / 2)
                    centerY = int((box[1][1] + box[3][1]) / 2)
                    depthToMine = depth_frame.get_distance(centerX, centerY)
                    if depthToMine == 0:
                        continue
                    print("depth to marker ->", depthToMine)
                    cv2.aruco.drawDetectedMarkers(color_frame, corners)
                else:
                    # turnSpeed = 5100
                    print("not mining area")
        except:
            # turnSpeed = 5050
            print("NO MARKER FOUND")

        tango.controller.setTarget(1, turnSpeed)

        return nextState