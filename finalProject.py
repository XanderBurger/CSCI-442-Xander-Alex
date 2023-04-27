import pyrealsense2 as rs
import cv2
import numpy as np
from maestro import Controller
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

align_to = rs.stream.color
align = rs.align(align_to)

width = 640
height = 480

tango = Controller()
BODY = 0
speed = 6000
turnSpeed = 6000
MOTORS = 1
TURN = 2
HEADTURN = 3

# Distance to stop
threshold_distance = 0.5  # in meters


def get_distance_to_blue_paper(cx, cy, depth_frame):
    # Get depth value at center of blue object
    depth_value = depth_frame.get_distance(cx, cy)
    # Convert depth value to meters
    distance = depth_value * 1000
    return distance


try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            continue

        frame = np.asanyarray(color_frame.get_data())
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # lower and upper bounds for blue
        # lower_blue = np.array([90, 50, 50])
        # upper_blue = np.array([130, 255, 255])

        # lower and upper bounds for neon green
        lower_green = np.array([60, 100, 100])
        upper_green = np.array([100, 255, 255])

        # mask for blue or green color
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # check for white binders
        hsv_white_lower = np.array([0, 0, 180])
        hsv_white_upper = np.array([255, 20, 255])
        mask_white = cv2.inRange(hsv, hsv_white_lower, hsv_white_upper)
        # white countours
        white_contours, hierarchy = cv2.findContours(mask_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in white_contours:
            area = cv2.contourArea(contour)
            if area > 5000:
                print("White binder detected, turning left")
                tango.setTarget(MOTORS, 6900)
                tango.setTarget(BODY, 5250)
                break

        # blue contours
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # moments/center
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # forward if the blue object is in center of frame
            if cx >= 250 and cx <= 350:
                print("Blue paper centered, moving forward")
                tango.setTarget(BODY, 5200)
                # check if robot within threshold distance of blue paper
                distance = get_distance_to_blue_paper(cx, cy, depth_frame)  # Use depth_frame to calculate distance
                if distance <= threshold_distance:
                    print("Reached blue paper, stopping")
                    tango.setTarget(BODY, 6000)
                    break
            # Otherwise, turn the robot left or right to look for the blue object
            elif cx < 250:
                print("Blue paper not centered, turning right")
                tango.setTarget(MOTORS, 5100)
            elif cx > 350:
                print("Blue paper not centered, turning left")
                tango.setTarget(MOTORS, 6900)

            # blue/white contours
            cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)
            cv2.drawContours(frame, white_contours, -1, (0, 255, 255), 2)

            cv2.imshow('contours', frame)
        else:
            tango.setTarget(MOTORS, 6900)
            # Exit with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                tango.setTarget(BODY, 6000)
                tango.setTarget(MOTORS, 6000)
                break

finally:
# Stop streaming
    pipeline.stop()
