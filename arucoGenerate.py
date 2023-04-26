import cv2
import numpy as np

markerSize = 200
markerImage22 = np.zeros((markerSize, markerSize), dtype=np.uint8)
markerImage49 = np.zeros((markerSize, markerSize), dtype=np.uint8)

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
cv2.aruco.generateImageMarker(aruco_dict, 22, 200, markerImage21)
cv2.imwrite("markerImage22.png", markerImage22)
cv2.aruco.generateImageMarker(aruco_dict, 49, 200, markerImage49)
cv2.imwrite("markerImage49.png", markerImage49)