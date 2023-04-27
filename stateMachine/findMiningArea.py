from state import State
import cv2

class FindMiningArea(State):
    
    def __init__(self) -> None:
        super().__init__()
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    def enterState(self, tango):
        pass

    def process(self, tango, color_frame, depth_frame):
        nextState = None
        corners, ids, rejected = cv2.aruco.detectMarkers(color_frame, self.aruco_dict)
        
        depthToMine = None

        if ids:
            for i in range(len(ids)):
                if ids[i] != 22:
                    turnSpeed = 6000
                    box = corners[i]
                    depthToMine = depth_frame.get_distance(int(
                    box[0]+box[2]/2), int(box[1]+box[3]/2)) 
                    print("found", depthToMine)
                    cv2.rectangle(color_frame, box[0], box[2], (255, 255, 0))
                    print("depth to marker ->", depthToMine)
                else:
                    turnSpeed = 5050
        else:
            turnSpeed = 5050
            print("NO MARKER FOUND")
    
        tango.setTarget(1, turnSpeed)

        return nextState