import pyrealsense2 as rs
import cv2
import numpy as np

from maestro import Controller

pipeline = rs.pipeline()
config = rs.config()
# state = stateMachine.StateMachine()

# Get device product line for setting a supporting resolution
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

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

width = 640
height = 480

tango = Controller()

FORWARD = 0
TURN = 1

speed = 6000
turnSpeed = 6000

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

try:
    while True:
        # Frames from camera
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            print("no Frames")
            continue
        frame = np.asanyarray(color_frame.get_data())
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Grayscale (better for edge detection)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        ret, thresh = cv2.threshold(blurred, 140, 255, cv2.THRESH_BINARY)

        mask = cv2.erode(thresh, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        print("Turn Right")
        corners, ids, rejected = cv2.aruco.detectMarkers(frame, aruco_dict)
        if ids:
            turnSpeed = 6000
            if ids[0] == 22:
                print("found maker 22")
        else:
            turnSpeed = 5050
    
        tango.setTarget(TURN, turnSpeed)

        # Show frames
        cv2.imshow('Original Frame', frame)

        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tango.setTarget(FORWARD, 6000)
            tango.setTarget(TURN, 6000)
            break

finally:
    # Stop streaming
    pipeline.stop()
