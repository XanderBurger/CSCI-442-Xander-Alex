import pyrealsense2 as rs
import cv2
import numpy as np
from maestro import Controller

'''Xander burger & Hoang Dang - CSCI442, Project 5 Pyrealsense line traversing'''

"""Most of this code is from the opencv_viewer_example from assigment sheet"""
# Configure depth and color stream

pipeline = rs.pipeline()
config = rs.config()

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
        # Normalize
        normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        # Gaussian blur
        blurred = cv2.GaussianBlur(normalized, (5, 5), 0)
        # Canny filter with larger kernel and squared pixels
        edges = cv2.Canny(blurred, 100, 200)
        edges = cv2.filter2D(edges, -1, np.array([[-1, -1, -1, -1, -1],
                                                   [-1, 0, 0, 0, -1],
                                                   [-1, 0, 16, 0, -1],
                                                   [-1, 0, 0, 0, -1],
                                                   [-1, -1, -1, -1, -1]]))
        edges = cv2.multiply(edges, edges)

        edges = cv2.threshold(edges, 40, 255, cv2.THRESH_BINARY)[1]

        # Show frames
        cv2.imshow('Original Frame', frame)
        cv2.imshow('Edge Detected Frame', edges)

        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


finally:
    # Stop streaming
    pipeline.stop()