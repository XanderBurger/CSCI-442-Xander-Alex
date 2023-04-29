import pyrealsense2 as rs
import cv2
import numpy as np
from miningTango import MiningTango

################################################
#              setting up pipeline             #
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

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

# Start streaming
pipeline.start(config)

rs.align(rs.stream.color)

width = 640
height = 480

################################################
#              Tango Settings                  #
################################################

tango = MiningTango("FIND MINE")
FORWARD = 0
TURN = 1

def get_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
        
        # Get the HSV value of the pixel at the clicked coordinates
        hsv_value = hsv_image[y, x]
        
        # Display the HSV value
        print(f"HSV value at ({x}, {y}): {hsv_value}")

try:
    while True:
        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            print("no Frames")
            continue

        color_image = np.asanyarray(color_frame.get_data())

        tango.process(color_image, depth_frame)

        cv2.setMouseCallback('Original Frame', get_hsv)
        cv2.imshow('Original Frame', color_image)

        
        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tango.controller.setTarget(FORWARD, 6000)
            tango.controller.setTarget(TURN, 6000)
            break
finally:
    tango.controller.setTarget(FORWARD, 6000)
    tango.controller.setTarget(TURN, 6000)
    pipeline.stop()
