import pyrealsense2 as rs
import cv2
import numpy as np

# from maestro import Controller
# from stateMachine import stateMachine


'''Xander burger & Hoang Dang - CSCI442, Project 5 Pyrealsense line traversing'''

"""Most of this code is from the opencv_viewer_example from assigment sheet"""
# Configure depth and color stream

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


def centerOfGravity(pixelArray):
    whitPixelsX = []
    whitPixelsY = []
    for x in range(width):
        for y in range(height):
            if pixelArray[y][x] == 255:
                whitPixelsX.append(x)
                whitPixelsY.append(y)

    return (int(sum(whitPixelsX) / len(whitPixelsX)), int(sum(whitPixelsY) / len(whitPixelsY)))


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

        ret, thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY_INV)

        mask = cv2.erode(thresh, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # Canny filter (seems to work better)
        # edges = cv2.Canny(blurred, 100, 200)
        # edgeArray = np.asanyarray(edges.get_data())
        contours, hierarchy = cv2.findContours(
            mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            # calculate moments
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            # calculate x,y coordinate of center

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.line(frame, (cX, 0), (cX, 720), (255, 0, 0), 1)
            cv2.line(frame, (0, cY), (1280, cY), (255, 0, 0), 1)

            cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)

            print(cX)
            print(cY)

            if cX >= 350:
                print("Turn Right")

            if cX < 350 and cX > 250:
                print("On Track!")

            if cX <= 250:
                print("Turn Left")

        # Show frames
        cv2.imshow('Original Frame', frame)

        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



finally:
    # Stop streaming
    pipeline.stop()