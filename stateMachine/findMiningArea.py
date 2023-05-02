from stateMachine.state import State
import cv2
import numpy as np

class FindMiningArea(State):
    
    def __init__(self) -> None:
        super().__init__()
        self.turning = True


    def enterState(self, tango):
        pass
    
    def process(self, tango, color_frame, depth_frame):
        nextState = None
        mat30 = np.full(color_frame.shape, 30, dtype=np.uint8)
        color_frame = cv2.add(color_frame, mat30)
        corners, ids, rejected = cv2.aruco.detectMarkers(color_frame, self.arucoDict)

        
        if tango.totalFrames % 30 == 0:
            self.turning = not self.turning

        try:
            for i in range(len(ids)):
                if int(ids[i]) == 49:
                    print("found mine")
                    box = corners[i][0]
                    centerX = int((box[0][0] + box[1][0]) / 2)
                    centerY = int((box[1][1] + box[3][1]) / 2)

                    if centerX >= 400:
                        self.turnSpeed = 5100
                    elif centerX <= 200:
                        self.turnSpeed = 6900
                    elif centerX < 400 and centerX > 200:
                        self.turnSpeed = 6000
                        return "GO TO MINE"

                    cv2.circle(color_frame, (centerX, centerY), 5, (255, 255, 0), 2)
                    cv2.aruco.drawDetectedMarkers(color_frame, corners)
                else:
                    if self.turning:
                        self.turnSpeed = 5100
                    else:
                        self.turnSpeed = 6000

        except TypeError:
            if self.turning:
                self.turnSpeed = 5100
            else:
                self.turnSpeed = 6000
            self.forwardSpeed = 6000
        
        tango.controller.setTarget(self.TURN, self.turnSpeed)
        tango.controller.setTarget(self.FORWARD, self.forwardSpeed)
        tango.totalFrames += 1
        
        return nextState
    
    def exitState(self, tango):
        pass