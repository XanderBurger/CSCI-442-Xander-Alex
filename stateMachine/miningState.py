from stateMachine.state import State
import cv2
import numpy as np
import time

class MiningState(State):
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        print("IN MINE")


    def process(self, tango, color_frame, depth_frame):
        nextState = None
        hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

        yellowBinary = cv2.inRange(hsv_frame, tango.yellowLower, tango.yellowUpper)
        greenBinary = cv2.inRange(hsv_frame, tango.greenLower, tango.greenUpper)
        pinkBinary = cv2.inRange(hsv_frame, tango.pinkLower, tango.pinkUpper)

        yellowContours, yellowHierarchy = cv2.findContours(yellowBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        greenContours, greenHierarchy = cv2.findContours(greenBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        pinkContours, pinkHierarchy = cv2.findContours(pinkBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(color_frame, yellowContours, -1, (255,255,0), 2)
        cv2.drawContours(color_frame, greenContours, -1, (0,255,0), 2)
        cv2.drawContours(color_frame, pinkContours, -1, (50, 0 ,255), 2)

        #do face detect stuff 
        faces = np.array([])
        try:
            gray = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
            faces = tango.face_cascade.detectMultiScale(gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            )
            
            faceY = None
            faceX = None
            faceW = None
            faceH = None

            for x, y, w, h in faces:
                faceY = y
                faceX = x
                faceW = w
                faceH = h
                cv2.rectangle(color_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        except:
            print("Face detection not working")
    
        if len(yellowContours) > 0:
            ycMax = max(yellowContours, key=cv2.contourArea)
            M = cv2.moments(ycMax)
            
            if M["m00"] != 0:
                ycX = int(M["m10"] / M["m00"])
                ycY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (ycX, ycY), 5, (255,255,0), 2)
                try:
                    if (ycY > faceY) and (ycX >= faceX) and (ycX <= faceX + faceW):
                        depthToYellow = depth_frame.get_distance(ycX, ycY)
                        print("PERSON HOLDING YELLOW")
                        if ycX >= 400:
                            self.turnSpeed = 5100
                        elif ycX <= 200:
                            self.turnSpeed = 6900
                        elif ycX < 400 and ycX > 200:
                            self.turnSpeed = 6000
                            if depthToYellow > 1:
                                self.forwardSpeed = 5100
                                self.turnSpeed = 6000
                            elif depthToYellow in range(0.1, 1):
                                self.forwardSpeed = 6000
                                self.turnSpeed = 6000
                                print("FOUND PERSON")
                                tango.iceBlockColor = "YELLOW"
                                return "FIND START"       
                except:
                    self.turnSpeed = 6000
                    self.forwardSpeed = 6000
                    print("no faces")

        
        if len(greenContours) > 0:
            gcMax = max(greenContours, key=cv2.contourArea)
            M = cv2.moments(gcMax)
            if M["m00"] != 0:
                gcX = int(M["m10"] / M["m00"])
                gcY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (gcX,gcY), 5, (255,255,0), 2)
                try:
                    if (gcY > faceY) and (gcX >= faceX) and (gcX <= faceX + faceW):
                        depthToGreen = depth_frame.get_distance(gcX, gcY)
                        print("PERSON HOLDING GREEN")
                        if gcX >= 400:
                            self.turnSpeed = 5100
                        elif gcX <= 200:
                            self.turnSpeed = 6900
                        elif gcX < 400 and gcX > 200:
                            self.turnSpeed = 6000
                            if depthToGreen > 1:
                                self.forwardSpeed = 5100
                                self.turnSpeed = 6000
                            elif depthToGreen in range(0.1, 1):
                                self.forwardSpeed = 6000
                                self.turnSpeed = 6000
                                print("FOUND PERSON")
                                tango.iceBlockColor = "GREEN"
                                return "FIND START"       
                except:
                    self.turnSpeed = 6000
                    self.forwardSpeed = 6000
                    print("no faces")
                

        if len(pinkContours) > 0:
            pcMax = max(pinkContours, key=cv2.contourArea)
            M = cv2.moments(pcMax)
            if M["m00"] != 0:
                pcX = int(M["m10"] / M["m00"])
                pcY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (pcX, pcY), 5, (255,255,0), 2)
                try:
                    if (pcY > faceY) and (pcX >= faceX) and (pcX <= faceX + faceW):
                        depthToPink = depth_frame.get_distance(pcX, pcY)
                        print("PERSON HOLDING PINK")
                        if pcX >= 400:
                            self.turnSpeed = 5100
                        elif pcX <= 200:
                            self.turnSpeed = 6900
                        elif pcX < 400 and pcX > 200:
                            self.turnSpeed = 6000
                            if depthToPink > 1:
                                self.forwardSpeed = 5100
                                self.turnSpeed = 6000
                            elif depthToPink in range(0.1, 1):
                                self.forwardSpeed = 6000
                                self.turnSpeed = 6000
                                print("FOUND PERSON")
                                tango.iceBlockColor = "PINK"
                                return "FIND START"       
                except:
                    self.turnSpeed = 6000
                    self.forwardSpeed = 6000
                    print("no faces")
                
            
        tango.controller.setTarget(self.FORWARD, self.forwardSpeed)
        tango.controller.setTarget(self.TURN, self.turnSpeed)

        return nextState

    
    def exitState(self, tango):
        pass