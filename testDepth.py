import pyrealsense2 as rs
import cv2
import numpy as np
from maestro import Controller

'''Xander burger & Hoang Dang - CSCI442, Project 4 Pyrealsense depth detection'''

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

"""gets the first frame from camera and instantiate the tracker"""
frames = pipeline.wait_for_frames()
color_frame = frames.get_color_frame()

if not color_frame:
    print("no Frames")

"""first frame as numpy array"""
color_image = np.asanyarray(color_frame.get_data())

'''Adjust brightness/contrast, not sure why image has green tint'''
a = 4.0  # Brightness control (1.0-3.0)
b = 75  # Contrast control (0-100)
color_image = cv2.convertScaleAbs(color_image, alpha=a, beta=b)

"""draw a bounding box around object to be tracked then hit enter"""
bbox = cv2.selectROI(color_image, False)

tracker = cv2.TrackerKCF_create()

ok = tracker.init(color_image, bbox)
depthList = []

startingDepth = None
tango = Controller()
motorStrength = 0
BODY = 0
threshold = 0.3

try:
    # Create a context object. This object owns the handles to all connected realsense devices
    startingDepth = None
    depthDiff = []
    for i in range(30):

        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        ok, bbox = tracker.update(color_image)

        if not depth or not ok:
            continue

        centerDepth = depth.get_distance(
            int(bbox[0]+bbox[2]/2), int(bbox[1]+bbox[3]/2))

        if centerDepth == 0:
            continue
        depthDiff.append(centerDepth)

    startingDepth = sum(depthDiff)/len(depthDiff)

    while True:
        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()

        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        ok, bbox = tracker.update(color_image)

        if not depth:
            continue

        objectCenter = (int(bbox[0]+bbox[2]/2), int(bbox[1]+bbox[3]/2))
        centerDepth = depth.get_distance(objectCenter[0], objectCenter[1])

        speed = 6000
        if centerDepth == 0 or not ok:
            tango.setTarget(BODY, speed)
            print("not OK")
            continue

        depthDiff = centerDepth - startingDepth
        print(depthDiff)

        if depthDiff > threshold:
            speed = 5250
            print("forwards")
        elif depthDiff < -threshold:
            speed = 6700
            print("backwards")
        else:
            speed = 6000

        tango.setTarget(BODY, speed)

        if (ok):
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(color_image, p1, p2, (0, 255, 0), 2, 1)
            cv2.circle(color_image, objectCenter, 25, (255, 0, 0), -1)

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', color_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            tango.setTarget(BODY, 6000)
            break

    exit(0)
# except rs.error as e:
#    # Method calls agaisnt librealsense objects may throw exceptions of type pylibrs.error
#    print("pylibrs.error was thrown when calling %s(%s):\n", % (e.get_failed_function(), e.get_failed_args()))
#    print("    %s\n", e.what())
#    exit(1)
except Exception as e:
    print(e)
    pass
