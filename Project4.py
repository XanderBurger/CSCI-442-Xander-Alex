import pyrealsense2 as rs
import numpy as np
import cv2
import maestro as controller

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

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            print("no Frames")
            continue

        # Convert images to numpy arrays
        """image being displayed"""
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
            depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # Tracking Object
        """updates tracker and returns a new bounding box around object"""
        ok, bbox = tracker.update(color_image)

        """drawing the bounding box on screen"""
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(color_image, p1, p2, (255, 0, 0), 2, 1)

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            print("resize")
            resized_color_image = cv2.resize(color_image, dsize=(
                depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)

            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        """This is the blank image below to video feeds, where the odometry stuff needs to be drawn."""
        blank_image = np.zeros(
            (color_image.shape[0], color_image.shape[1] * 2, 3), dtype=np.uint8)
        object_corners = ((bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]))
        object_width = bbox[2] - bbox[0]

        """The get_distance() methods called on the depth_frame takes an x and y and returns the depth at that point"""
        depthThresh = 0.2
        depth_to_object = depth_frame.get_distance(int(
            bbox[0]+bbox[2]/2), int(bbox[1]+bbox[3]/2))  # use the center of the bounding box
        '''check if values are within depth threshold'''
        if depth_to_object < depthThresh:
            depth_to_object = depthThresh
        elif depth_to_object > depthThresh + 1.0:
            depth_to_object = depthThresh + 1.0
        depthList.append(depth_to_object)
        if len(depthList) > 15:
            depthList.pop(0)
        '''Smooth out depth with recent depth values'''
        finDepth = sum(depthList) / len(depthList)

        """Setting a starting depth to compare to"""
        # this might need to be ran for a few frames so we get a more accurate starting depth
        if not startingDepth:
            startingDepth = finDepth

        """controlling the robot"""
        depthDiff = startingDepth - finDepth

        motorStrength = 0

        # this might need to be adjusted to a larger threshold
        if depthDiff > 1:
            motorStrength = 3000
            print("forwards")

        elif depthDiff < 0.5:
            motorStrength = -3000
            print("backwards")

        # print(depthDiff)

        """drawing on lower screen"""
        center = (int(blank_image.shape[0]/2), int(blank_image.shape[1]/2))
        cv2.rectangle(
            blank_image, (center[1]-10, center[0]-10), (center[1]+10, center[0]+10),  (0, 255, 0),  2, 1)

        '''Adjust scaling factor to smooth axis changes'''
        scaling = 250
        '''Draw line with respect to bbox and depth'''
        xStart = bbox[0] - int(finDepth * scaling) + 300
        xEnd = bbox[0] + bbox[2] - int(finDepth * scaling)
        y = int(center[0] - finDepth * scaling)
        cv2.line(blank_image, (xStart, y), (xEnd, y), (255, 0, 0))

        images = np.vstack((images, blank_image))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
