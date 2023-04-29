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

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 60)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

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
threshold_distance = 0.25  # in meters
threshold_distance_initial = 1.0  # in meters
cv2.namedWindow('contours')

def get_distance(cx, cy, depth_frame):
    # Get depth value at center of object
    depth_value = depth_frame.get_distance(cx, cy)
    # Convert depth value to meters
    distance = depth_value * 1000
    return distance


# Blue color bounds
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

# Green color bounds
lower_green = np.array([60, 100, 100])
upper_green = np.array([100, 255, 255])

# Orange color bounds
lower_orange = np.array([5, 100, 100])
upper_orange = np.array([15, 255, 255])

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            continue

        frame = np.asanyarray(color_frame.get_data())
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Mask for blue, green, and orange colors
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
        mask = mask_blue + mask_green + mask_orange

        # Check for colors
        blue_contours, hierarchy = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        green_contours, hierarchy = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        orange_contours, hierarchy = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        tango.setTarget(BODY, speed)
        tango.setTarget(MOTORS, turnSpeed)

        if len(blue_contours) > 0:
            # find the largest contour
            c = max(blue_contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # check if the blue object is within threshold distance
            distance = get_distance(cx, cy, depth_frame)
            if distance <= threshold_distance_initial:
                while True:
                    # check if the robot is within stop threshold distance
                    distance = get_distance(cx, cy, depth_frame)
                    if cx >= 250 and cx <= 350:
                        print("Blue paper centered, moving forward")
                        speed = 5200
                        if distance <= threshold_distance:
                            print("Reached blue paper, stopping")
                            tango.setTarget(BODY, 6000)
                            tango.setTarget(MOTORS, 6000)
                            break
                    elif cx < 250:
                        print("Blue paper not centered, turning right")
                        turnSpeed = 5100
                    elif cx > 350:
                        print("Blue paper not centered, turning left")
                        turnSpeed = 6900

                    cv2.drawContours(frame, blue_contours, -1, (255, 0, 0), 2)




        if len(green_contours) > 0:
            # find the largest contour
            c = max(blue_contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # check if the green object is within threshold distance
            distance = get_distance(cx, cy, depth_frame)
            if distance <= threshold_distance_initial:
                while True:
                    # check if the robot is within stop threshold distance
                    distance = get_distance(cx, cy, depth_frame)
                    if cx >= 250 and cx <= 350:
                        print("Green paper centered, moving forward")
                        speed = 5200
                        if distance <= threshold_distance:
                            print("Reached green paper, stopping")
                            tango.setTarget(BODY, 6000)
                            tango.setTarget(MOTORS, 6000)
                            break
                    elif cx < 250:
                        print("Green paper not centered, turning right")
                        turnSpeed = 5100
                    elif cx > 350:
                        print("Green paper not centered, turning left")
                        turnSpeed = 6900

                    cv2.drawContours(frame, green_contours, -1, (0, 255, 0), 2)




        ##        elif len(orange_contours) > 0:
        ##            # find the largest contour
        ##            c = max(blue_contours, key=cv2.contourArea)
        ##            M = cv2.moments(c)
        ##            if M["m00"] != 0: # add this conditional statement to check for zero division
        ##                cx = int(M["m10"] / M["m00"])
        ##                cy = int(M["m01"] / M["m00"])
        ##            else:
        ##                cx, cy = 0, 0 # set default values if there is a zero division
        ##        else:
        ##            cx, cy = 0, 0 # set default values if no contours are detected

        if len(orange_contours) > 0:
            # find the largest contour
            c = max(blue_contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # check if the green object is within threshold distance
            distance = get_distance(cx, cy, depth_frame)
            if distance <= threshold_distance_initial:
                while True:
                    # check if the robot is within stop threshold distance
                    distance = get_distance(cx, cy, depth_frame)
                    if cx >= 250 and cx <= 350:
                        print("Orange paper centered, moving forward")
                        speed = 5200
                        if distance <= threshold_distance:
                            print("Orange green paper, stopping")
                            tango.setTarget(BODY, 6000)
                            tango.setTarget(MOTORS, 6000)
                            break
                    elif cx < 250:
                        print("Orange paper not centered, turning right")
                        turnSpeed = 5100
                    elif cx > 350:
                        print("Orange paper not centered, turning left")
                        turnSpeed = 6900

                    cv2.drawContours(frame, green_contours, -1, (0, 0, 255), 2)


        else:
            print("None Found, Turning")
            turnSpeed = 6900

        cv2.imshow('contours', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tango.setTarget(BODY, 6000)
            tango.setTarget(MOTORS, 6000)
            break


finally:
    # Stop streaming
    tango.setTarget(BODY, 6000)
    tango.setTarget(MOTORS, 6000)
    pipeline.stop()

