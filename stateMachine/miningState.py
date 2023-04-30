from stateMachine.state import State
import cv2
import numpy as np
import time

class MiningState(State):
    def __init__(self) -> None:
        super().__init__()

    def enterState(self, tango):
        # time.sleep(1.7)
        # tango.controller.setTarget(self.FORWARD, 6000)
        tango.controller.setTarget(self.HEADTILT, 6000)
        print("IN MINE")


    def process(self, tango, color_frame, depth_frame):
        nextState = None
        hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

        yellowBinary = cv2.inRange(hsv_frame, tango.yellowLower, tango.yellowUpper)
        greenBinary = cv2.inRange(hsv_frame, tango.greenLower, tango.greenUpper)
        pinkBinary = cv2.inRange(hsv_frame, tango.pinkLower, tango.pinkUpper)
        orangeBinary = cv2.inRange(hsv_frame, tango.orangeLower, tango.orangeUpper)
        blueBinary = cv2.inRange(hsv_frame, tango.blueLower, tango.blueUpper)

        yellowContours, yellowHierarchy = cv2.findContours(yellowBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        greenContours, greenHierarchy = cv2.findContours(greenBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        pinkContours, pinkHierarchy = cv2.findContours(pinkBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        orangeContours, orangeHierarchy = cv2.findContours(orangeBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        blueContours, blueHierarchy = cv2.findContours(blueBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(color_frame, yellowContours, -1, (255,255,0), 2)
        cv2.drawContours(color_frame, greenContours, -1, (0,255,0), 2)
        cv2.drawContours(color_frame, pinkContours, -1, (50, 0 ,255), 2)
        cv2.drawContours(color_frame, orangeContours, -1, (255, 0 ,255), 2)
        cv2.drawContours(color_frame, blueContours, -1, (255, 0 , 0), 2)

        #do face detect stuff 
        faces = np.array([])
        try:
            gray = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
            # mat30 = np.full(gray.shape, 30, dtype=np.uint8)
            # gray = cv2.add(gray, mat30)
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
                        tango.iceBlockColor = "YELLOW"
                        print("PERSON HOLDING YELLOW")
                        if ycX >= 350:
                            self.turnSpeed = 5050
                        elif ycX <= 250:
                            self.turnSpeed = 6950
                        elif ycX < 350 and ycX > 250:
                            self.turnSpeed = 6000
                            if depthToYellow > 1:
                                self.forwardSpeed = 5100
                                self.turnSpeed = 6000
                            else:
                                self.forwardSpeed = 6000
                                self.turnSpeed = 6000
                                print("found Mine")
                                # nextState = "MINING AREA"
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
                        tango.iceBlockColor = "GREEN"
                        print("PERSON HOLDING GREEN")
                        # return "FIND START"
                except:
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
                        tango.iceBlockColor = "PINK"
                        print("PERSON HOLDING PINK")
                        # return "FIND START"
                except:
                    print("no faces")
            
        if len(orangeContours) > 0:
            ocMax = max(orangeContours, key=cv2.contourArea)
            M = cv2.moments(ocMax)
            if M["m00"] != 0:
                ocX = int(M["m10"] / M["m00"])
                ocY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (ocX, ocY), 5, (255,255,0), 2)
    
        if len(blueContours) > 0:
            bcMax = max(blueContours, key=cv2.contourArea)
            M = cv2.moments(bcMax)
            if M["m00"] != 0:
                bcX = int(M["m10"] / M["m00"])
                bcY = int(M["m01"] / M["m00"])
                cv2.circle(color_frame, (bcX, bcY), 5, (255,255,0), 2)
        
        tango.controller.setTarget(self.FORWARD, self.forwardSpeed)
        tango.controller.setTarget(self.TURN, self.turnSpeed)
        # nextState = "FIND START"
        return nextState

    
    def exitState(self, tango):
        pass