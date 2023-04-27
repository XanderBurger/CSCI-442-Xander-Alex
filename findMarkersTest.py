import pyrealsense2 as rs
import cv2
import numpy as np
from maestro import Controller


################################################
#              setting up pipeline
################################################

pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

align_to = rs.stream.color
align = rs.align(align_to)

width = 640
height = 480

################################################
#              Tango Settings
################################################

tango = Controller()
FORWARD = 0
TURN = 1
speed = 6000
turnSpeed = 6000

arucoNumMeaning = {
    22: "MINING AREA",
    49: "STARTING AREA"
}

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

try:
    while True:
        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            print("no Frames")
            continue

        color_image = np.asanyarray(color_frame.get_data())
  
        corners, ids, rejected = cv2.aruco.detectMarkers(color_image, aruco_dict)
        
        depthToBackWall = None
        depthToFrontWall = None

        if ids.any():
            turnSpeed = 6000
            for i in range(len(ids)):
                id = int(ids[i])
                nameOfMarker = arucoNumMeaning[id]
                print("found", nameOfMarker)
                box = corners[i][0]
                print(box)
                print(box[0][0])
                centerX = int((box[0][0] + box[1][0]) / 2)
                centerY = int((box[1][1] + box[3][1]) / 2)
                depthToMarker = depth_frame.get_distance(centerX, centerY)
                print("depth to marker ->", depthToMarker)
                
                #cv2.rectangle(color_image, int(box[0][0], box[0][1]), int(box[3][0], box[3][1]), (0, 255, 0), 3, 1)
                
                cv2.aruco.drawDetectedMarkers(color_image, corners)
                if nameOfMarker == "MINING AREA":
                    depthToFrontWall = depthToFrontWall
                elif nameOfMarker == "STARTING AREA":
                    depthToBackWall = depthToMarker
        else:
           # turnSpeed = 5050
            print("NO MARKER FOUND")
    
        tango.setTarget(TURN, turnSpeed)
        cv2.imshow('Original Frame', color_image)

        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tango.setTarget(FORWARD, 6000)
            tango.setTarget(TURN, 6000)
            break
finally:
    tango.setTarget(FORWARD, 6000)
    tango.setTarget(TURN, 6000)
    pipeline.stop()
